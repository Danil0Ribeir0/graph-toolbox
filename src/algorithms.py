class GraphTraversal:
    @staticmethod
    def is_connected(graph):
        nodes = graph.get_nodes()
        if not nodes: return True
        
        visited = set()
        start_node = nodes[0]
        
        def dfs(v):
            visited.add(v)
            for neighbor in graph.get_neighbors(v):
                if neighbor not in visited:
                    dfs(neighbor)
        
        dfs(start_node)
        return len(visited) == len(nodes)