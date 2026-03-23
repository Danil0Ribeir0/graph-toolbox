from typing import Dict, List, Optional, Set, Tuple, Hashable

class Graph:
    def __init__(self, directed: bool=False) -> None:
        self.adj_list: Dict[Hashable, Dict[Hashable, float]] = {}
        self.directed: bool = directed

    def add_edge(self, u: Hashable, v: Hashable, weight: float = 1.0) -> None:
        if u not in self.adj_list:
            self.adj_list[u] = {}
        if v not in self.adj_list:
            self.adj_list[v] = {}

        self.adj_list[u][v] = float(weight)
        if not self.directed:
            self.adj_list[v][u] = float(weight)

    def get_nodes(self) -> List[Hashable]:
        return list(self.adj_list.keys())

    def get_neighbors(self, node: Hashable) -> List[Hashable]:
        return list(self.adj_list.get(node, {}).keys())

    def get_weight(self, u: Hashable, v: Hashable) -> Optional[float]:
        return self.adj_list.get(u, {}).get(v)

    def total_weight(self) -> float:
        total: float = 0.0
        seen_edges: Set[Tuple[str, str]] = set()
        
        for u in self.adj_list:
            for v, weight in self.adj_list[u].items():
                edge = tuple(sorted((str(u), str(v))))
                if edge not in seen_edges:
                    total += weight
                    seen_edges.add(edge)
        return total
