"""Simulate forwarding decision based on routing table."""
from app.models.routing_table import RoutingTable
from app.utils.logger import logger


class ForwardingService:
    def __init__(self, routing_table: RoutingTable):
        self.routing_table = routing_table

    def get_next_hop(self, destination: str) -> str:
        for entry in self.routing_table.entries:
            if entry.destination == destination:
                logger.info(f"Forward to {destination} via {entry.next_hop}")
                return entry.next_hop
        logger.warning(f"No route to {destination}")
        return None
