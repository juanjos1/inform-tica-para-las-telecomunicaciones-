"""Top-level router application controller: wires all services together."""
from app.models.router import Router
from app.network.controller_connection import ControllerConnection
from app.services.registration_service import RegistrationService
from app.services.neighbor_service import NeighborService
from app.services.routing_table_service import RoutingTableService
from app.services.forwarding_service import ForwardingService
from app.controllers.registration_controller import RegistrationController
from app.controllers.neighbor_controller import NeighborController
from app.controllers.routing_table_controller import RoutingTableController
from app.controllers.forwarding_controller import ForwardingController
from app.dao import router_config_dao
from app.utils.logger import logger


class RouterAppController:
    def __init__(self, router_id: str, ip: str, port: int,
                 controller_host: str, controller_port: int, protocol: str = "tcp"):

        # Error #5: load persisted config if it exists and matches the given ID
        saved_cfg = router_config_dao.load_config()
        if saved_cfg.get("router_id") == router_id:
            # Re-use persisted IP, port and protocol (CLI args may omit them)
            ip       = saved_cfg.get("ip",       ip)
            port     = saved_cfg.get("port",      port)
            protocol = saved_cfg.get("protocol",  protocol)
            logger.info(
                f"Router '{router_id}' already exists in config — "
                f"reusing saved settings (ip={ip}, port={port}, protocol={protocol})."
            )
        else:
            logger.info(f"No existing config for '{router_id}'; creating new router instance.")

        self.router = Router(router_id, ip, port)
        connection = ControllerConnection(controller_host, controller_port, protocol)

        reg_svc  = RegistrationService(connection)
        # Pass router_id so NeighborService can validate self-loops (#7)
        nb_svc   = NeighborService(connection, router_id=router_id)
        rt_svc   = RoutingTableService(router_id)
        fwd_svc  = ForwardingService(rt_svc.routing_table)

        self.registration_ctrl   = RegistrationController(reg_svc)
        self.neighbor_ctrl       = NeighborController(nb_svc)
        self.routing_table_ctrl  = RoutingTableController(rt_svc)
        self.forwarding_ctrl     = ForwardingController(fwd_svc)

        logger.info(f"Router {router_id} initialised, controller at {controller_host}:{controller_port}")

