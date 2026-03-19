import heapq


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
    def dijkstra(graph, start_node):
        distances = {node: float("inf") for node in graph.get_nodes()}
        distances[start_node] = 0

        priority_queue = [(0, start_node)]

        while priority_queue:
            current_distance, u = heapq.heappop(priority_queue)

            if current_distance > distances[u]:
                continue

            for v in graph.get_neighbors(u):
                weight = graph.get_weight(u, v)
                distance = current_distance + weight

                if distance < distances[v]:
                    distances[v] = distance
                    heapq.heappush(priority_queue, (distance, v))

        return distances
