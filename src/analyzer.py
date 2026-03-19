class Graph:
    def __init__(self):
        self.adj_list = {}

    def add_node(self, node):
        if node not in self.adj_list:
            self.adj_list[node] = []

    def add_edge(self, u, v):
        self.add_node(u)
        self.add_node(v)
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def get_degree(self, node):
        return len(self.adj_list.get(node, []))

    def has_eulerian_cycle(self):
        if not self.adj_list:
            return False
        
        for node, edges in self.adj_list.items():
            if len(edges) % 2 != 0:
                return False
        return True