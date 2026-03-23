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

    def test_get_nodes_returns_all_unique_nodes(self, empty_graph):
        empty_graph.add_edge(1, 2)
        empty_graph.add_edge(2, 3)
        nodes = empty_graph.get_nodes()
        assert len(nodes) == 3
        assert set(nodes) == {1, 2, 3}

    def test_is_connected_returns_true_for_connected_graph(self, simple_weighted_graph):
        assert simple_weighted_graph.is_connected() is True

    def test_is_connected_returns_false_for_disconnected_graph(
        self, disconnected_graph
    ):
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

    def test_prim_mst_total_weight(self):
        g = Graph()
        g.add_edge("A", "B", 1.0)
        g.add_edge("B", "C", 5.0)
        g.add_edge("C", "A", 10.0)

        mst = SpanningTree.prim(g, "A")

        assert mst.total_weight() == 6.0
        assert len(mst.get_nodes()) == 3


class TestEulerianValidator:
    def test_has_cycle_true_when_connected_and_even_degrees(self, cycle_graph):
        assert EulerianValidator.has_cycle(cycle_graph) is True

    def test_has_cycle_false_when_odd_degrees_exist(self, empty_graph):
        empty_graph.add_edge("A", "B")
        empty_graph.add_edge("B", "C")
        assert EulerianValidator.has_cycle(empty_graph) is False

    def test_has_cycle_false_when_disconnected_even_with_even_degrees(self):
        g = Graph()

        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)

        g.add_edge(4, 5)
        g.add_edge(5, 6)
        g.add_edge(6, 4)

        assert EulerianValidator.has_cycle(g) is False
