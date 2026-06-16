"""Computes and stores routing tables (FR-04, FR-05)."""
from app.models.topology import Topology
from app.services.routing_table_service import build_all_routing_tables
from app.dao import routing_table_dao, log_dao
from app.utils.logger import logger


class RoutingController:
    def __init__(self):
        self.routing_tables: dict = {}

    def compute_all(self, topology: Topology):
        self.routing_tables = build_all_routing_tables(topology)
        routing_table_dao.save_routing_tables(self.routing_tables)
        log_dao.append_log("ROUTE_COMPUTATION", {"nodes": list(self.routing_tables.keys())})
        logger.info(f"Routing tables computed for: {list(self.routing_tables.keys())}")

    def get_table(self, router_id: str):
        return self.routing_tables.get(router_id)
