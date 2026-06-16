"""Handles topology updates from routers (FR-02, FR-03)."""
from app.models.topology import Topology
from app.services.topology_service import TopologyService


class TopologyController:
    def __init__(self, topology: Topology):
        self.service = TopologyService(topology)

    def handle_topology_update(self, router_id: str, neighbors: list):
        self.service.update_neighbors(router_id, neighbors)

    def handle_router_removal(self, router_id: str) -> bool:
        """Remove router_id from the topology graph (all edges included)."""
        return self.service.remove_router(router_id)

    def handle_link_cost_update(self, source: str, destination: str, new_cost: float):
        self.service.update_link_cost(source, destination, new_cost)

    @property
    def topology(self) -> Topology:
        return self.service.topology
