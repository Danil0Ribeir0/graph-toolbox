import json
import warnings
from collections import deque
from typing import Dict, List, Optional, Set, Tuple, Hashable, Iterable


class Graph:
    def __init__(self, directed: bool = False) -> None:
        self.adj_list: Dict[Hashable, Dict[Hashable, float]] = {}
        self.in_degrees: Dict[Hashable, int] = {}
        self.directed: bool = directed
        self._connection_cache: Dict[str, bool] = {}

    def add_edge(self, u: Hashable, v: Hashable, weight: float = 1.0) -> None:
        if u is None or v is None:
            raise ValueError("Os nós do grafo não podem ser nulos (None).")
        if u == "" or v == "":
            raise ValueError("Os nós do grafo não podem ser strings vazias.")
            
        try:
            weight_float = float(weight)
        except (TypeError, ValueError):
            raise ValueError(f"O peso da aresta tem de ser um número válido. Recebido: {weight}")

        if u not in self.adj_list:
            self.adj_list[u] = {}
            self.in_degrees[u] = 0
        if v not in self.adj_list:
            self.adj_list[v] = {}
            self.in_degrees[v] = 0

        is_new_edge = v not in self.adj_list[u]
        
        if not is_new_edge:
            warnings.warn(
                f"A aresta {u}->{v} já existe. O peso foi sobrescrito para {weight_float}.",
                UserWarning
            )

        self.adj_list[u][v] = weight_float
        
        if is_new_edge:
            self.in_degrees[v] += 1

        if not self.directed:
            self.adj_list[v][u] = weight_float
            if is_new_edge:
                self.in_degrees[u] += 1
                
        self._connection_cache.clear()
    
    def remove_edge(self, u: Hashable, v: Hashable) -> None:
        if u not in self.adj_list or v not in self.adj_list[u]:
            raise KeyError(f"A aresta {u}->{v} não existe no grafo.")

        del self.adj_list[u][v]
        self.in_degrees[v] -= 1

        if not self.directed:
            if v in self.adj_list and u in self.adj_list[v]:
                del self.adj_list[v][u]
                self.in_degrees[u] -= 1

        self._connection_cache.clear()

    def get_nodes(self) -> List[Hashable]:
        return list(self.adj_list.keys())

    def get_neighbors(self, node: Hashable) -> Iterable[Hashable]:
        return self.adj_list.get(node, {}).keys()
    
    def get_weight(self, u: Hashable, v: Hashable) -> Optional[float]:
        return self.adj_list.get(u, {}).get(v)

    def total_weight(self) -> float:
        total: float = 0.0

        if self.directed:
            for u in self.adj_list:
                total += sum(self.adj_list[u].values())
            return total

        seen_edges: Set[Tuple[Hashable, Hashable]] = set()
        
        for u in self.adj_list:
            for v, weight in self.adj_list[u].items():
                edge = (u, v) if hash(u) < hash(v) else (v, u)
                
                if edge not in seen_edges:
                    total += weight
                    seen_edges.add(edge)
                    
        return total

    def is_connected(self, connection_type: str = "strong") -> bool:
        if connection_type in self._connection_cache:
            return self._connection_cache[connection_type]
        
        nodes = self.get_nodes()
        if not nodes:
            return False

        if not self.directed:
            result = len(self.bfs(nodes[0])) == len(nodes)
        elif connection_type == "strong":
            result = self._is_strongly_connected(nodes)
        elif connection_type == "weak":
            result = self._is_weakly_connected(nodes)
        else:
            raise ValueError("connection_type deve ser 'strong' ou 'weak'.")

        self._connection_cache[connection_type] = result
        return result

    def strongly_connected_components(self) -> List[List[Hashable]]:
        nodes = self.get_nodes()
        if not nodes:
            return []

        visited: Set[Hashable] = set()
        finish_order: List[Hashable] = []

        for node in nodes:
            if node not in visited:
                stack = [(node, False)]
                while stack:
                    current, visited_neighbors = stack.pop()
                    if visited_neighbors:
                        finish_order.append(current)
                    else:
                        if current not in visited:
                            visited.add(current)
                            stack.append((current, True))
                            for neighbor in self.get_neighbors(current):
                                if neighbor not in visited:
                                    stack.append((neighbor, False))

        reversed_adj: Dict[Hashable, List[Hashable]] = {n: [] for n in nodes}
        for u in self.adj_list:
            for v in self.adj_list[u]:
                reversed_adj[v].append(u)

        sccs: List[List[Hashable]] = []
        visited_reversed: Set[Hashable] = set()

        for node in reversed(finish_order):
            if node not in visited_reversed:
                component: List[Hashable] = []
                stack_rev = [node]
                while stack_rev:
                    current = stack_rev.pop()
                    if current not in visited_reversed:
                        visited_reversed.add(current)
                        component.append(current)
                        for neighbor in reversed_adj[current]:
                            if neighbor not in visited_reversed:
                                stack_rev.append(neighbor)
                sccs.append(component)

        return sccs

    def _is_strongly_connected(self, nodes: List[Hashable]) -> bool:
        sccs = self.strongly_connected_components()
        return len(sccs) == 1 if sccs else True

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
        result: List[Hashable] = []
        stack: List[Hashable] = [start_node]

        while stack:
            current = stack.pop()
            if current not in visited:
                visited.add(current)
                result.append(current)

                for neighbor in self.get_neighbors(current):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return result

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
