"""Tests for communication controller (FR-01..FR-08, NFR-05)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest, json
from unittest.mock import patch, MagicMock
from app.controllers.controller_app_controller import ControllerAppController
from app.utils.json_utils import encode_message, decode_message
from app.utils.constants import MSG_REGISTER, MSG_TOPOLOGY, MSG_ACK, MSG_ERROR


class TestCommunicationController(unittest.TestCase):
    def setUp(self):
        with patch("app.dao.router_dao.load_routers", return_value={}), \
             patch("app.dao.topology_dao.load_topology"), \
             patch("app.dao.router_dao.save_routers"), \
             patch("app.dao.topology_dao.save_topology"), \
             patch("app.dao.routing_table_dao.save_routing_tables"), \
             patch("app.dao.log_dao.append_log"):
            self.app = ControllerAppController()
            self.comm = self.app.get_comm_controller()

    def _send(self, msg: dict) -> dict:
        with patch("app.dao.router_dao.save_routers"), \
             patch("app.dao.topology_dao.save_topology"), \
             patch("app.dao.routing_table_dao.save_routing_tables"), \
             patch("app.dao.log_dao.append_log"):
            raw = encode_message(msg)
            response = self.comm.handle(raw)
            return decode_message(response)

    def test_register_router_returns_ack(self):
        msg = {"type": MSG_REGISTER, "router_id": "R1", "ip": "127.0.0.1", "port": 5001}
        resp = self._send(msg)
        self.assertEqual(resp["type"], MSG_ACK)

    def test_duplicate_register_same_router_returns_error(self):
        """Same router sending REGISTER_ROUTER twice (e.g. pressing menu option 1 again)."""
        msg = {"type": MSG_REGISTER, "router_id": "R1", "ip": "127.0.0.1", "port": 5001}
        first = self._send(msg)
        second = self._send(msg)
        self.assertEqual(first["type"], MSG_ACK)
        self.assertEqual(second["type"], MSG_ERROR)

    def test_duplicate_register_different_instance_returns_error(self):
        """A different instance trying to reuse an already-registered router_id."""
        self._send({"type": MSG_REGISTER, "router_id": "R1", "ip": "127.0.0.1", "port": 5001})
        resp = self._send({"type": MSG_REGISTER, "router_id": "R1", "ip": "10.0.0.5", "port": 6000})
        self.assertEqual(resp["type"], MSG_ERROR)
        # Registry must keep the first registration untouched
        router = self.app.registry.get_router("R1")
        self.assertEqual((router.ip, router.port), ("127.0.0.1", 5001))

    def test_invalid_json_returns_error(self):
        response = self.comm.handle(b"not json at all!!!")
        resp = decode_message(response)
        self.assertEqual(resp["type"], MSG_ERROR)

    def test_unknown_type_returns_error(self):
        msg = {"type": "UNKNOWN_MSG"}
        resp = self._send(msg)
        self.assertEqual(resp["type"], MSG_ERROR)

    def test_topology_update_triggers_route_computation(self):
        # Register router first
        self._send({"type": MSG_REGISTER, "router_id": "R1", "ip": "127.0.0.1", "port": 5001})
        self._send({"type": MSG_REGISTER, "router_id": "R2", "ip": "127.0.0.1", "port": 5002})
        resp = self._send({
            "type": "TOPOLOGY_UPDATE",
            "router_id": "R1",
            "neighbors": [{"neighbor_id": "R2", "cost": 5}]
        })
        # Should return routing table or ack
        self.assertIn(resp["type"], ["ROUTING_TABLE", "ACK"])


if __name__ == "__main__":
    unittest.main()
