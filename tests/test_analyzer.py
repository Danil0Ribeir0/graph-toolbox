from src.analyzer import Graph

def test_add_nodes_and_edges():
    g = Graph()
    g.add_edge('A', 'B')
    assert 'A' in g.adj_list
    assert 'B' in g.adj_list

def test_get_degree():
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('A', 'C')
    assert g.get_degree('A') == 2
    assert g.get_degree('B') == 1

def test_eulerian_cycle_true():
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    g.add_edge('C', 'A')
    assert g.has_eulerian_cycle() == True

def test_eulerian_cycle_false():
    g = Graph()
    g.add_edge('A', 'B')
    g.add_edge('B', 'C')
    assert g.has_eulerian_cycle() == False