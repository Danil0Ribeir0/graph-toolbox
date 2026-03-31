from src.models import Graph


class EulerianValidator:
    @staticmethod
    def has_eulerian_cycle(graph: Graph) -> bool:
        if not graph.is_connected():
            return False

        for node in graph.get_nodes():
            if graph.get_degree(node) % 2 != 0:
                return False
        return True
