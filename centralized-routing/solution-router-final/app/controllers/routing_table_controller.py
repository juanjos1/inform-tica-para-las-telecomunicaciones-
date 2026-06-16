"""Handle incoming routing table from controller (FR-06)."""
from app.services.routing_table_service import RoutingTableService


class RoutingTableController:
    def __init__(self, service: RoutingTableService):
        self.service = service

    def receive_routing_table(self, entries: list):
        self.service.update(entries)

    def get_table(self):
        return self.service.get_table()
