import pytest
from src.models import Graph
from src.algorithms import PathFinder, SpanningTree
from src.validator import EulerianValidator


@pytest.fixture
def empty_graph() -> Graph:
    """Retorna um grafo vazio não direcionado."""
    return Graph()


@pytest.fixture
def simple_weighted_graph() -> Graph:
    """Retorna um grafo com pesos para testes de caminho mínimo."""
    g = Graph()
    g.add_edge("A", "B", 1.0)
    g.add_edge("B", "C", 2.0)
    g.add_edge("A", "C", 10.0)
    return g


@pytest.fixture
def disconnected_graph() -> Graph:
    """Retorna um grafo desconexo (duas ilhas)."""
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(3, 4)
    return g


@pytest.fixture
def cycle_graph() -> Graph:
    """Retorna um grafo que forma um ciclo perfeito (graus pares)."""
    g = Graph()
    g.add_edge("A", "B")
    g.add_edge("B", "C")
    g.add_edge("C", "D")
    g.add_edge("D", "A")
    return g


@pytest.fixture
def empty_directed_graph() -> Graph:
    """Retorna um grafo vazio direcionado."""
    return Graph(directed=True)


class TestGraphModels:
    def test_add_edge_creates_undirected_connection(self, empty_graph):
        empty_graph.add_edge("A", "B")
        assert "B" in empty_graph.get_neighbors("A")
        assert "A" in empty_graph.get_neighbors("B")
    
    def test_add_edge_warns_on_overwrite(self, empty_graph):
        import warnings

        empty_graph.add_edge("A", "B", 5.0)
        
        with pytest.warns(UserWarning, match="já existe. O peso foi sobrescrito"):
            empty_graph.add_edge("A", "B", 10.0)
            
        assert empty_graph.get_weight("A", "B") == 10.0

    def test_get_nodes_returns_all_unique_nodes(self, empty_graph):
        empty_graph.add_edge(1, 2)
        empty_graph.add_edge(2, 3)
        nodes = empty_graph.get_nodes()
        assert len(nodes) == 3
        assert set(nodes) == {1, 2, 3}

    def test_empty_graph_is_not_connected(self, empty_graph):
        assert empty_graph.is_connected() is False

    def test_is_connected_returns_true_for_connected_graph(self, simple_weighted_graph):
        assert simple_weighted_graph.is_connected() is True

    def test_is_connected_returns_false_for_disconnected_graph(self, disconnected_graph):
        assert disconnected_graph.is_connected() is False

    def test_degrees_undirected_graph(self, empty_graph):
        empty_graph.add_edge("A", "B")
        empty_graph.add_edge("A", "C")

        assert empty_graph.get_degree("A") == 2
        assert empty_graph.get_in_degree("A") == 2
        assert empty_graph.get_out_degree("A") == 2

    def test_degrees_directed_graph(self, empty_directed_graph):
        empty_directed_graph.add_edge("A", "B")  # A -> B
        empty_directed_graph.add_edge("C", "A")  # C -> A

        assert empty_directed_graph.get_in_degree("A") == 1
        assert empty_directed_graph.get_out_degree("A") == 1
        assert empty_directed_graph.get_degree("A") == 2

        assert empty_directed_graph.get_in_degree("B") == 1
        assert empty_directed_graph.get_out_degree("B") == 0
    
    def test_directed_graph_strong_connectivity(self, empty_directed_graph):
        empty_directed_graph.add_edge("A", "B")
        empty_directed_graph.add_edge("B", "C")
        empty_directed_graph.add_edge("C", "A")
        assert empty_directed_graph.is_connected(connection_type="strong") is True

    def test_directed_graph_not_strongly_connected(self, empty_directed_graph):
        empty_directed_graph.add_edge("A", "B")
        empty_directed_graph.add_edge("B", "C")
        assert empty_directed_graph.is_connected(connection_type="strong") is False

    def test_directed_graph_weak_connectivity(self, empty_directed_graph):
        empty_directed_graph.add_edge("A", "B")
        empty_directed_graph.add_edge("C", "B")
        
        assert empty_directed_graph.is_connected(connection_type="strong") is False
        assert empty_directed_graph.is_connected(connection_type="weak") is True


class TestGraphAlgorithms:
    def test_dijkstra_shortest_path(self, simple_weighted_graph):
        distancias = PathFinder.dijkstra(simple_weighted_graph, "A")
        assert distancias["C"] == 3.0

    def test_dijkstra_raises_error_for_negative_weights(self, simple_weighted_graph):
        simple_weighted_graph.add_edge("C", "D", -5.0)
        
        with pytest.raises(ValueError, match="pesos negativos"):
            PathFinder.dijkstra(simple_weighted_graph, "A")
    
    def test_dijkstra_filters_unreachable_nodes(self, empty_graph):
        empty_graph.add_edge("A", "B", 2.0)
        empty_graph.add_edge("C", "D", 1.0) 
        
        distances = PathFinder.dijkstra(empty_graph, "A")
        
        assert "B" in distances
        assert distances["B"] == 2.0
        assert "C" not in distances
        assert "D" not in distances

    def test_dijkstra_raises_error_for_nonexistent_start_node(self, empty_graph):
        empty_graph.add_edge("A", "B", 1.0)
        
        with pytest.raises(ValueError, match="não existe no grafo"):
            PathFinder.dijkstra(empty_graph, "Z")

    def test_prim_mst_total_weight(self):
        g = Graph()
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 5.0)
        g.add_edge("C", "A", 10.0)

        mst = SpanningTree.prim(g, "A")

        assert mst.total_weight() == 6.0
        assert len(mst.get_nodes()) == 3
    
    def test_prim_raises_error_for_directed_graph(self, empty_directed_graph):
        """Garante que o Algoritmo de Prim rejeita grafos direcionados."""
        empty_directed_graph.add_edge("A", "B", 1.0)
        empty_directed_graph.add_edge("B", "C", 2.0)
        
        with pytest.raises(ValueError, match="não direcionados"):
            SpanningTree.prim(empty_directed_graph, "A")


class TestEulerianValidator:
    def test_has_cycle_true_when_connected_and_even_degrees(self, cycle_graph):
        assert EulerianValidator.has_eulerian_cycle(cycle_graph) is True

    def test_has_cycle_false_when_odd_degrees_exist(self, empty_graph):
        empty_graph.add_edge("A", "B")
        empty_graph.add_edge("B", "C")
        assert EulerianValidator.has_eulerian_cycle(empty_graph) is False

    def test_has_cycle_false_when_disconnected_even_with_even_degrees(self):
        g = Graph()

        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)

        g.add_edge(4, 5)
        g.add_edge(5, 6)
        g.add_edge(6, 4)

        assert EulerianValidator.has_eulerian_cycle(g) is False


class TestGraphSerialization:
    def test_to_dict_format(self, simple_weighted_graph):
        data = simple_weighted_graph.to_dict()

        assert data["directed"] is False
        assert "A" in data["adj_list"]
        assert data["adj_list"]["A"]["B"] == 1.0
    
    def test_from_dict_reconstruction(self):
        data = {
            "directed": True,
            "adj_list": {
                "X": {"Y": 5.0},
                "Y": {}
            }
        }
        
        g = Graph.from_dict(data)
        
        assert g.directed is True
        assert g.get_weight("X", "Y") == 5.0
        assert g.get_in_degree("Y") == 1
        assert g.get_out_degree("X") == 1

    def test_json_save_and_load(self, simple_weighted_graph, tmp_path):
        filepath = tmp_path / "meu_grafo.json"
        
        simple_weighted_graph.save_to_json(filepath)
        assert filepath.exists()
        
        loaded_graph = Graph.load_from_json(filepath)
        
        assert loaded_graph.directed == simple_weighted_graph.directed
        assert loaded_graph.get_weight("A", "C") == 10.0
        assert loaded_graph.get_degree("B") == 2
