"""Manage and send neighbor information (FR-02)."""
from typing import List
from app.models.neighbor import Neighbor
from app.network.controller_connection import ControllerConnection
from app.utils.constants import MSG_TOPOLOGY
from app.utils.logger import logger
from app.dao import neighbor_dao


class NeighborService:
    def __init__(self, connection: ControllerConnection, router_id: str = ""):
        self.connection = connection
        self.router_id = router_id
        self.neighbors: List[Neighbor] = neighbor_dao.load_neighbors()

    def add_neighbor(self, neighbor_id: str, cost: float) -> tuple[bool, str]:
        """Add a neighbor. Returns (success, message)."""
        # Error #7: prevent adding self as neighbor
        if neighbor_id == self.router_id:
            return False, f"Cannot add yourself ({self.router_id}) as a neighbor."

        # Error #8: reject duplicates instead of silently replacing
        existing = next((n for n in self.neighbors if n.neighbor_id == neighbor_id), None)
        if existing is not None:
            return False, (
                f"Neighbor '{neighbor_id}' already exists with cost {existing.cost}. "
                f"Remove it first if you want to update it."
            )

        self.neighbors.append(Neighbor(neighbor_id, cost))
        neighbor_dao.save_neighbors(self.neighbors)
        return True, f"Neighbor '{neighbor_id}' added with cost {cost}."

    def update_neighbor_cost(self, neighbor_id: str, new_cost: float) -> tuple[bool, str]:
        """Update the cost of an existing neighbor locally and persist. Returns (success, message)."""
        neighbor = next((n for n in self.neighbors if n.neighbor_id == neighbor_id), None)
        if neighbor is None:
            return False, f"Neighbor '{neighbor_id}' not found."
        neighbor.cost = new_cost
        neighbor_dao.save_neighbors(self.neighbors)
        logger.info(f"Local link cost updated: {self.router_id}->{neighbor_id} = {new_cost}")
        return True, f"Local cost to '{neighbor_id}' updated to {new_cost}."

    def remove_neighbor(self, neighbor_id: str) -> tuple[bool, str]:
        """Remove a neighbor by ID. Returns (success, message)."""
        # Error #3: explicit deletion method
        before = len(self.neighbors)
        self.neighbors = [n for n in self.neighbors if n.neighbor_id != neighbor_id]
        if len(self.neighbors) == before:
            return False, f"Neighbor '{neighbor_id}' not found."
        neighbor_dao.save_neighbors(self.neighbors)
        return True, f"Neighbor '{neighbor_id}' removed."

    def send_neighbors(self, router_id: str) -> dict:
        msg = {
            "type": MSG_TOPOLOGY,
            "router_id": router_id,
            "neighbors": [n.to_dict() for n in self.neighbors],
        }
        response = self.connection.send(msg)
        logger.info(f"Topology sent, response: {response.get('type')}")
        return response
