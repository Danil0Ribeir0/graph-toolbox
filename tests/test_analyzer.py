from src.models import Graph
from src.validator import EulerianValidator
from src.algorithms import GraphTraversal

def test_graph_connectivity():
    g = Graph()
    g.add_edge(1, 2)
    g.add_edge(3, 4)
    assert GraphTraversal.is_connected(g) == False

def test_eulerian_with_connectivity():
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('C', 'D')
    g.add_edge('D', 'A')
    assert EulerianValidator.has_cycle(g) == True