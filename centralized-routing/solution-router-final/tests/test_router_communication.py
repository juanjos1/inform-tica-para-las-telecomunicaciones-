"""Integration-style tests for router communication flow."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import MagicMock, patch
from app.services.registration_service import RegistrationService
from app.services.neighbor_service import NeighborService
from app.services.routing_table_service import RoutingTableService


class TestRouterCommunicationFlow(unittest.TestCase):
    def test_full_flow_register_send_topology_receive_table(self):
        conn = MagicMock()
        conn.send.side_effect = [
            {"type": "ACK", "info": "Router R1 registered"},  # registration
            {  # topology update
                "type": "ROUTING_TABLE",
                "router_id": "R1",
                "routing_table": [
                    {"destination": "R2", "next_hop": "R2", "cost": 5},
                ]
            },
        ]
        with patch("app.services.registration_service.log_dao.append_log"), \
             patch("app.services.neighbor_service.neighbor_dao.load_neighbors", return_value=[]), \
             patch("app.services.neighbor_service.neighbor_dao.save_neighbors"), \
             patch("app.services.routing_table_service.routing_table_dao.save_routing_table"):

            reg_svc = RegistrationService(conn)
            ok = reg_svc.register("R1", "127.0.0.1", 5001)
            self.assertTrue(ok)

            nb_svc = NeighborService(conn)
            nb_svc.add_neighbor("R2", 5)
            response = nb_svc.send_neighbors("R1")

            rt_svc = RoutingTableService("R1")
            rt_svc.update(response.get("routing_table", []))
            self.assertEqual(len(rt_svc.get_table().entries), 1)


if __name__ == "__main__":
    unittest.main()
