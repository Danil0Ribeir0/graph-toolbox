import heapq
from typing import Dict, Optional, Tuple, Hashable, List, Set
from src.models import Graph


class GraphTraversal:
    @staticmethod
    def is_connected(graph):
        nodes = graph.get_nodes()
        if not nodes:
            return True

        visited = set()
        start_node = nodes[0]

        def dfs(v):
            visited.add(v)
            for neighbor in graph.get_neighbors(v):
                if neighbor not in visited:
                    dfs(neighbor)

        dfs(start_node)
        return len(visited) == len(nodes)


class PathFinder:
    @staticmethod
    def dijkstra(graph: Graph, start_node: Hashable) -> Dict[Hashable, float]:
        distances: Dict[Hashable, float] = {node: float("inf") for node in graph.get_nodes()}
        distances[start_node] = 0.0

        priority_queue: List[Tuple[float, Hashable]] = [(0.0, start_node)]

        while priority_queue:
            current_distance, u = heapq.heappop(priority_queue)

            if current_distance > distances[u]:
                continue

            for v in graph.get_neighbors(u):
                weight = graph.get_weight(u, v)
                if weight is not None:
                    distance = current_distance + weight

                    if distance < distances[v]:
                        distances[v] = distance
                        heapq.heappush(priority_queue, (distance, v))

        return distances


class SpanningTree:
    @staticmethod
    def prim(graph: Graph, start_node: Hashable) -> Graph:
        g = Graph()
        visited: Set[Hashable] = set()

        priority_queue: List[Tuple[float, Optional[Hashable], Hashable]] = [(0.0, None, start_node)]

        while priority_queue and len(visited) < len(graph.get_nodes()):
            weight, u, v = heapq.heappop(priority_queue)

            if v in visited:
                continue

            visited.add(v)

            if u is not None:
                g.add_edge(u, v, weight)

            for neighbor in graph.get_neighbors(v):
                if neighbor not in visited:
                    w = graph.get_weight(v, neighbor)
                    if w is not None:
                        heapq.heappush(priority_queue, (w, v, neighbor))

        return g
