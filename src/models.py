import json
import warnings
from collections import deque
from typing import Dict, List, Optional, Set, Tuple, Hashable


class Graph:
    def __init__(self, directed: bool = False) -> None:
        self.adj_list: Dict[Hashable, Dict[Hashable, float]] = {}
        self.in_degrees: Dict[Hashable, int] = {}
        self.directed: bool = directed

    def add_edge(self, u: Hashable, v: Hashable, weight: float = 1.0) -> None:
        if u not in self.adj_list:
            self.adj_list[u] = {}
            self.in_degrees[u] = 0
        if v not in self.adj_list:
            self.adj_list[v] = {}
            self.in_degrees[v] = 0

        is_new_edge = v not in self.adj_list[u]
        
        if not is_new_edge:
            warnings.warn(
                f"A aresta {u}->{v} já existe. O peso foi sobrescrito para {weight}.",
                UserWarning
            )

        self.adj_list[u][v] = float(weight)
        
        if is_new_edge:
            self.in_degrees[v] += 1

        if not self.directed:
            self.adj_list[v][u] = float(weight)
            if is_new_edge:
                self.in_degrees[u] += 1

    def get_nodes(self) -> List[Hashable]:
        return list(self.adj_list.keys())

    def get_neighbors(self, node: Hashable) -> List[Hashable]:
        return list(self.adj_list.get(node, {}).keys())

    def get_weight(self, u: Hashable, v: Hashable) -> Optional[float]:
        return self.adj_list.get(u, {}).get(v)

    def total_weight(self) -> float:
        total: float = 0.0

        if self.directed:
            for u in self.adj_list:
                total += sum(self.adj_list[u].values())
            return total

        seen_edges: Set[frozenset] = set()

        for u in self.adj_list:
            for v, weight in self.adj_list[u].items():
                edge = frozenset([u, v])
                if edge not in seen_edges:
                    total += weight
                    seen_edges.add(edge)

        return total

    def is_connected(self, connection_type: str = "strong") -> bool:
        nodes = self.get_nodes()
        if not nodes:
            return False

        if not self.directed:
            return len(self.bfs(nodes[0])) == len(nodes)

        if connection_type == "strong":
            return self._is_strongly_connected(nodes)
        elif connection_type == "weak":
            return self._is_weakly_connected(nodes)
        else:
            raise ValueError("connection_type deve ser 'strong' ou 'weak'.")

    def _is_strongly_connected(self, nodes: List[Hashable]) -> bool:
        start_node = nodes[0]

        if len(self.bfs(start_node)) != len(nodes):
            return False

        reversed_adj_list: Dict[Hashable, List[Hashable]] = {node: [] for node in nodes}
        for u in self.adj_list:
            for v in self.adj_list[u]:
                reversed_adj_list[v].append(u)

        visited: Set[Hashable] = {start_node}
        queue: deque = deque([start_node])
        while queue:
            current = queue.popleft()
            for neighbor in reversed_adj_list[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return len(visited) == len(nodes)

    def _is_weakly_connected(self, nodes: List[Hashable]) -> bool:
        visited: Set[Hashable] = {nodes[0]}
        queue: deque = deque([nodes[0]])
        
        while queue:
            current = queue.popleft()
            
            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
                    
            for u in self.adj_list:
                if current in self.adj_list[u] and u not in visited:
                    visited.add(u)
                    queue.append(u)
                    
        return len(visited) == len(nodes)

    def get_out_degree(self, node: Hashable) -> int:
        return len(self.adj_list.get(node, {}))

    def get_in_degree(self, node: Hashable) -> int:
        return self.in_degrees.get(node, 0)

    def get_degree(self, node: Hashable) -> int:
        if not self.directed:
            return self.get_out_degree(node)
        return self.get_in_degree(node) + self.get_out_degree(node)

    def bfs(self, start_node: Hashable) -> List[Hashable]:
        if start_node not in self.adj_list:
            return []

        visited: Set[Hashable] = {start_node}
        queue: deque = deque([start_node])
        traversal_order: List[Hashable] = []

        while queue:
            current = queue.popleft()
            traversal_order.append(current)

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return traversal_order

    def dfs(self, start_node: Hashable) -> List[Hashable]:
        if start_node not in self.adj_list:
            return []

        visited: Set[Hashable] = set()
        stack: List[Hashable] = [start_node]
        traversal_order: List[Hashable] = []

        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                traversal_order.append(current)

                for neighbor in reversed(self.get_neighbors(current)):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return traversal_order

    def to_dict(self) -> dict:
        return {
            "directed": self.directed,
            "adj_list": self.adj_list
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Graph':
        if "directed" not in data:
            raise ValueError("O dicionário/JSON fornecido não contém a chave obrigatória 'directed'.")
        if not isinstance(data["directed"], bool):
            raise TypeError(f"A chave 'directed' deve ser um booleano (True/False), mas recebeu {type(data['directed']).__name__}.")
        
        directed = data.get("directed", False)
        g = cls(directed=directed)
        
        adj_list = data.get("adj_list", {})
        
        for node in adj_list:
            if node not in g.adj_list:
                g.adj_list[node] = {}
                g.in_degrees[node] = 0

        for u, neighbors in adj_list.items():
            for v, weight in neighbors.items():
                if v not in g.adj_list[u]:
                    g.add_edge(u, v, weight)
                
        return g
    
    def save_to_json(self, filepath: str) -> None:
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, indent=4)
    
    @classmethod
    def load_from_json(cls, filepath: str) -> 'Graph':
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_dict(data)
