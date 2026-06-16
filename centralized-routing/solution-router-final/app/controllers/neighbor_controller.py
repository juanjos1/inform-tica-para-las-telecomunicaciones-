"""Neighbor controller (FR-02)."""
from app.services.neighbor_service import NeighborService


class NeighborController:
    def __init__(self, service: NeighborService):
        self.service = service

    def add_neighbor(self, neighbor_id: str, cost: float) -> tuple[bool, str]:
        return self.service.add_neighbor(neighbor_id, cost)

    def remove_neighbor(self, neighbor_id: str) -> tuple[bool, str]:
        return self.service.remove_neighbor(neighbor_id)

    def send_to_controller(self, router_id: str) -> dict:
        return self.service.send_neighbors(router_id)
