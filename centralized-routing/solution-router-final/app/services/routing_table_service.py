"""Store and retrieve the local routing table (FR-06)."""
from app.models.routing_table import RoutingTable
from app.dao import routing_table_dao
from app.utils.logger import logger


class RoutingTableService:
    def __init__(self, router_id: str):
        self.routing_table = RoutingTable(router_id)

    def update(self, entries: list):
        self.routing_table.update_from_list(entries)
        routing_table_dao.save_routing_table(self.routing_table)
        logger.info(f"Routing table updated: {len(entries)} entries")

    def get_table(self) -> RoutingTable:
        return self.routing_table
