import heapq
from typing import Dict, Optional, Tuple, Hashable, List, Set
from src.models import Graph


class PathFinder:
    @staticmethod
    def dijkstra(graph: Graph, start_node: Hashable) -> Tuple[Dict[Hashable, float], Dict[Hashable, List[Hashable]]]:
        if start_node not in graph.get_nodes():
            raise ValueError(f"O nó de partida '{start_node}' não existe no grafo.")

        distances: Dict[Hashable, float] = {node: float("inf") for node in graph.get_nodes()}
        distances[start_node] = 0.0
        
        predecessors: Dict[Hashable, Optional[Hashable]] = {node: None for node in graph.get_nodes()}

        priority_queue: List[Tuple[float, Hashable]] = [(0.0, start_node)]

        while priority_queue:
            current_distance, u = heapq.heappop(priority_queue)

            if current_distance > distances[u]:
                continue

            for v in graph.get_neighbors(u):
                weight = graph.get_weight(u, v)
                if weight is not None:
                    if weight < 0:
                        raise ValueError(f"O Algoritmo de Dijkstra não suporta arestas com pesos negativos (Aresta {u}->{v} tem peso {weight}).")

                    distance = current_distance + weight

                    if distance < distances[v]:
                        distances[v] = distance
                        predecessors[v] = u
                        heapq.heappush(priority_queue, (distance, v))

        reachable_distances = {}
        paths = {}
        
        for node, dist in distances.items():
            if dist != float("inf"):
                reachable_distances[node] = dist
                
                path = []
                current = node
                while current is not None:
                    path.append(current)
                    current = predecessors.get(current)
                path.reverse()
                paths[node] = path

        return reachable_distances, paths


class SpanningTree:
    @staticmethod
    def prim(graph: Graph, start_node: Hashable) -> Graph:
        if graph.directed:
            raise ValueError("O Algoritmo de Prim suporta apenas grafos não direcionados.")
        
        g = Graph()
        visited: Set[Hashable] = set()

        priority_queue: List[Tuple[float, Optional[Hashable], Hashable]] = [
            (0.0, None, start_node)
        ]

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
