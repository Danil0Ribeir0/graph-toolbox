class Graph:
    def __init__(self, directed=False):
        self.adj_list = {}
        self.directed = directed

    def add_edge(self, u, v):
        for node in [u, v]:
            if node not in self.adj_list:
                self.adj_list[node] = set()

        self.adj_list[u].add(v)
        if not self.directed:
            self.adj_list[v].add(u)

    def get_nodes(self):
        return list(self.adj_list.keys())

    def get_neighbors(self, node):
        return self.adj_list.get(node, set())
