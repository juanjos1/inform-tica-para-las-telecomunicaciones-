"""Orchestrates all incoming messages from routers (FR-01..FR-08, NFR-05)."""
import json
from app.controllers.router_registry_controller import RouterRegistryController
from app.controllers.topology_controller import TopologyController
from app.controllers.routing_controller import RoutingController
from app.services.message_service import ack_message, error_message, routing_table_message
from app.network.client_handler import send_routing_table
from app.utils.constants import MSG_REGISTER, MSG_TOPOLOGY, MSG_LINK_COST
from app.utils.logger import logger
from app.utils.json_utils import decode_message, encode_message


class CommunicationController:
    def __init__(self, registry: RouterRegistryController,
                 topology_ctrl: TopologyController,
                 routing_ctrl: RoutingController):
        self.registry = registry
        self.topology_ctrl = topology_ctrl
        self.routing_ctrl = routing_ctrl

    def handle(self, raw: bytes) -> bytes:
        """Parse raw bytes, dispatch to correct handler, return response bytes."""
        try:
            msg = decode_message(raw)
        except (ValueError, UnicodeDecodeError) as e:
            logger.warning(f"Invalid JSON received: {e}")
            return encode_message(error_message("Invalid JSON"))

        msg_type = msg.get("type")

        if msg_type == MSG_REGISTER:
            return self._handle_register(msg)
        elif msg_type == MSG_TOPOLOGY:
            return self._handle_topology(msg)
        elif msg_type == MSG_LINK_COST:
            return self._handle_link_cost(msg)
        else:
            logger.warning(f"Unknown message type: {msg_type}")
            return encode_message(error_message(f"Unknown type: {msg_type}"))

    def _handle_register(self, msg: dict) -> bytes:
        router_id = msg.get("router_id")
        ip = msg.get("ip")
        port = msg.get("port")
        if not all([router_id, ip, port]):
            return encode_message(error_message("Missing fields in REGISTER_ROUTER"))

        if not self.registry.register(router_id, ip, int(port)):
            logger.warning(f"Duplicate REGISTER_ROUTER rejected for router_id '{router_id}'")
            return encode_message(error_message(f"Router ID '{router_id}' is already registered"))

        self.topology_ctrl.topology.add_router(router_id)
        return encode_message(ack_message(f"Router {router_id} registered"))

    def _handle_topology(self, msg: dict) -> bytes:
        router_id = msg.get("router_id")
        neighbors = msg.get("neighbors", [])
        if not router_id:
            return encode_message(error_message("Missing router_id in TOPOLOGY_UPDATE"))

        self.topology_ctrl.handle_topology_update(router_id, neighbors)
        # Recompute routing tables after topology change
        self.routing_ctrl.compute_all(self.topology_ctrl.topology)

        # --- Fix #6: notify affected neighbors ---
        # When R1 declares R2 as a neighbor, R2 must also learn about the
        # relationship and receive its updated routing table automatically.
        # We use the existing send_routing_table() / client_handler to push
        # the table to every neighbor that is already registered.
        for neighbor_entry in neighbors:
            neighbor_id = neighbor_entry.get("neighbor_id")
            cost = float(neighbor_entry.get("cost", 1))
            if not neighbor_id:
                continue

            neighbor_router = self.registry.get_router(neighbor_id)
            if neighbor_router is None:
                # Neighbor not yet registered — nothing to notify yet
                logger.info(
                    f"Neighbor '{neighbor_id}' declared by '{router_id}' is not yet "
                    f"registered; skipping notification."
                )
                continue

            # Mirror the edge: ensure the topology also reflects R2->R1
            # (bidirectional link with the same cost) only if R2 has not
            # already declared R1 as its own neighbor in the topology.
            existing_edges = self.topology_ctrl.topology.get_neighbors(neighbor_id)
            already_declared = any(n == router_id for n, _ in existing_edges)
            if not already_declared:
                self.topology_ctrl.topology.graph[neighbor_id].append((router_id, cost))
                logger.info(
                    f"Auto-mirrored edge {neighbor_id}->{router_id} (cost={cost}) "
                    f"in topology graph."
                )
                # Recompute again now that the reverse edge is in place
                self.routing_ctrl.compute_all(self.topology_ctrl.topology)

            # Push the updated routing table to the neighbor router
            neighbor_table = self.routing_ctrl.get_table(neighbor_id)
            if neighbor_table:
                payload = routing_table_message(
                    neighbor_id,
                    [e.to_dict() for e in neighbor_table.entries]
                )
                send_routing_table(neighbor_router.ip, neighbor_router.port, payload)
                logger.info(
                    f"Routing table pushed to neighbor '{neighbor_id}' "
                    f"({neighbor_router.ip}:{neighbor_router.port}) "
                    f"after '{router_id}' declared it as neighbor."
                )
        # --- End Fix #6 ---

        # Send updated table to the requesting router (original behaviour)
        table = self.routing_ctrl.get_table(router_id)
        if table:
            return encode_message(routing_table_message(router_id, [e.to_dict() for e in table.entries]))
        return encode_message(ack_message("Topology updated"))

    def _handle_link_cost(self, msg: dict) -> bytes:
        source = msg.get("source")
        destination = msg.get("destination")
        cost = msg.get("cost")
        if not all([source, destination, cost is not None]):
            return encode_message(error_message("Missing fields in LINK_COST_UPDATE"))

        self.topology_ctrl.handle_link_cost_update(source, destination, float(cost))
        # Also mirror the reverse edge so the topology stays bidirectional
        self.topology_ctrl.handle_link_cost_update(destination, source, float(cost))

        self.routing_ctrl.compute_all(self.topology_ctrl.topology)

        # Push updated routing tables to every registered router so that all
        # nodes reflect the new link cost immediately — identical to what
        # _handle_topology does for neighbor registration changes.
        for router_id in self.topology_ctrl.topology.get_nodes():
            router_info = self.registry.get_router(router_id)
            if router_info is None:
                continue
            table = self.routing_ctrl.get_table(router_id)
            if table:
                payload = routing_table_message(
                    router_id,
                    [e.to_dict() for e in table.entries]
                )
                send_routing_table(router_info.ip, router_info.port, payload)
                logger.info(
                    f"Routing table pushed to '{router_id}' "
                    f"({router_info.ip}:{router_info.port}) after link cost update "
                    f"{source}->{destination}={cost}."
                )

        return encode_message(ack_message("Link cost updated and routes recalculated"))
