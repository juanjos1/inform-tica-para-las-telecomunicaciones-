"""Topology model: adjacency-list graph of the network (FR-03)."""
from typing import Dict, List, Tuple


class Topology:
    def __init__(self):
        self.graph: Dict[str, List[Tuple[str, float]]] = {}

    def add_router(self, router_id: str):
        if router_id not in self.graph:
            self.graph[router_id] = []

    def update_neighbors(self, router_id: str, neighbors: List[dict]):
        """Replace the neighbor list for router_id (FR-02, FR-03)."""
        self.add_router(router_id)
        self.graph[router_id] = []
        for n in neighbors:
            neighbor_id = n["neighbor_id"]
            cost = float(n["cost"])
            self.add_router(neighbor_id)
            self.graph[router_id].append((neighbor_id, cost))

    def update_link_cost(self, source: str, destination: str, new_cost: float):
        """Update a specific link cost (FR-08)."""
        if source in self.graph:
            self.graph[source] = [
                (n, new_cost if n == destination else c)
                for n, c in self.graph[source]
            ]

    def remove_router(self, router_id: str) -> bool:
        """Remove router_id and every edge that references it (FR-09).

        Deletes:
        - The node's own adjacency list (all outgoing edges).
        - Every entry in other nodes' lists whose neighbor == router_id
          (all incoming edges).

        Returns True if the router existed and was removed, False otherwise.
        """
        if router_id not in self.graph:
            return False
        del self.graph[router_id]
        for node in self.graph:
            self.graph[node] = [
                (n, c) for n, c in self.graph[node] if n != router_id
            ]
        return True

    def get_nodes(self) -> List[str]:
        return list(self.graph.keys())

    def get_neighbors(self, router_id: str) -> List[Tuple[str, float]]:
        return self.graph.get(router_id, [])

    def to_dict(self) -> dict:
        return {k: [{"neighbor": n, "cost": c} for n, c in v] for k, v in self.graph.items()}
