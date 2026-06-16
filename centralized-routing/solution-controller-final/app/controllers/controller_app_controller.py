"""Top-level application controller: wires everything together."""
from app.models.topology import Topology
from app.controllers.router_registry_controller import RouterRegistryController
from app.controllers.topology_controller import TopologyController
from app.controllers.routing_controller import RoutingController
from app.controllers.communication_controller import CommunicationController
from app.dao import topology_dao
from app.utils.logger import logger


class ControllerAppController:
    def __init__(self):
        topology = topology_dao.load_topology()
        self.registry = RouterRegistryController()
        self.topology_ctrl = TopologyController(topology)
        self.routing_ctrl = RoutingController()
        self.comm_ctrl = CommunicationController(
            self.registry, self.topology_ctrl, self.routing_ctrl
        )
        logger.info("Controller application initialised")

    def remove_router(self, router_id: str) -> bool:
        """Full cascade removal of a router (FR-09).

        Steps in order:
          1. Validate presence in the registry.
          2. Deregister (persists routers.json).
          3. Remove node + all edges from the topology graph (persists topology.json).
          4. Recompute routing tables for every remaining node (persists routing_tables.json).

        Returns True on success, False if the router was not registered.
        """
        if not self.registry.is_registered(router_id):
            logger.warning(f"remove_router: '{router_id}' is not registered — nothing to remove")
            return False

        self.registry.remove_router(router_id)
        self.topology_ctrl.handle_router_removal(router_id)
        self.routing_ctrl.compute_all(self.topology_ctrl.topology)

        logger.info(
            f"Router '{router_id}' fully removed: registry + topology + routing tables recomputed"
        )
        return True

    def get_comm_controller(self) -> CommunicationController:
        return self.comm_ctrl
