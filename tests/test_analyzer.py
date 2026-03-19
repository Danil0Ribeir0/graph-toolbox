from src.models import Graph
from src.algorithms import GraphTraversal
from src.validator import EulerianValidator


class TestGraphModels:
    def test_add_edge_creates_undirected_connection(self):
        g = Graph(directed=False)

        g.add_edge("A", "B")

        assert "B" in g.get_neighbors("A")
        assert "A" in g.get_neighbors("B")

    def test_get_nodes_returns_all_unique_nodes(self):
        g = Graph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)

        nodes = g.get_nodes()
        assert len(nodes) == 3
        assert set(nodes) == {1, 2, 3}


class TestGraphAlgorithms:
    def test_is_connected_returns_true_for_connected_graph(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")

        assert GraphTraversal.is_connected(g) is True

    def test_is_connected_returns_false_for_disconnected_graph(self):
        g = Graph()
        g.add_edge(1, 2)
        g.add_edge(3, 4)

        assert GraphTraversal.is_connected(g) is False


class TestEulerianValidator:
    def test_has_cycle_true_when_connected_and_even_degrees(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")
        g.add_edge("C", "D")
        g.add_edge("D", "A")

        assert EulerianValidator.has_cycle(g) is True

    def test_has_cycle_false_when_odd_degrees_exist(self):
        g = Graph()
        g.add_edge("A", "B")
        g.add_edge("B", "C")

        assert EulerianValidator.has_cycle(g) is False

    def test_has_cycle_false_when_disconnected_even_with_even_degrees(self):
        g = Graph()
        g.add_edge(1, 2)
        g.add_edge(2, 3)
        g.add_edge(3, 1)

        g.add_edge(4, 5)
        g.add_edge(5, 6)
        g.add_edge(6, 4)

        assert EulerianValidator.has_cycle(g) is False
