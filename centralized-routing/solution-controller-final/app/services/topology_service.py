"""Topology service: update topology and persist it."""
from app.models.topology import Topology
from app.dao import topology_dao
from app.utils.logger import logger
from app.dao import log_dao


class TopologyService:
    def __init__(self, topology: Topology):
        self.topology = topology

    def update_neighbors(self, router_id: str, neighbors: list):
        self.topology.update_neighbors(router_id, neighbors)
        topology_dao.save_topology(self.topology)
        log_dao.append_log("TOPOLOGY_UPDATE", {"router_id": router_id})
        logger.info(f"Topology updated for {router_id}: {neighbors}")

    def remove_router(self, router_id: str) -> bool:
        """Remove router from the topology graph and persist the change."""
        removed = self.topology.remove_router(router_id)
        if removed:
            topology_dao.save_topology(self.topology)
            log_dao.append_log("TOPOLOGY_ROUTER_REMOVED", {"router_id": router_id})
            logger.info(f"Router '{router_id}' removed from topology")
        else:
            logger.warning(f"remove_router: '{router_id}' was not in the topology graph")
        return removed

    def update_link_cost(self, source: str, destination: str, new_cost: float):
        self.topology.update_link_cost(source, destination, new_cost)
        topology_dao.save_topology(self.topology)
        log_dao.append_log("LINK_COST_UPDATE", {"source": source, "destination": destination, "cost": new_cost})
        logger.info(f"Link cost updated {source}->{destination}: {new_cost}")
