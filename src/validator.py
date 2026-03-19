from .algorithms import GraphTraversal

class EulerianValidator:
    @staticmethod
    def has_cycle(graph):
        if not GraphTraversal.is_connected(graph):
            return False
        
        for node in graph.get_nodes():
            if len(graph.get_neighbors(node)) % 2 != 0:
                return False
        return True