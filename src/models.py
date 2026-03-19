class Graph:
    def __init__(self, directed=False):
        self.adj_list = {}
        self.directed = directed

    def add_edge(self, u, v, weight=1):
        if u not in self.adj_list:
            self.adj_list[u] = {}
        if v not in self.adj_list:
            self.adj_list[v] = {}

        self.adj_list[u][v] = weight
        if not self.directed:
            self.adj_list[v][u] = weight

    def get_nodes(self):
        return list(self.adj_list.keys())

    def get_neighbors(self, node):
        return list(self.adj_list.get(node, {}).keys())
    
    def get_weight(self, u, v):
        return self.adj_list.get(u, {}).get(v)
