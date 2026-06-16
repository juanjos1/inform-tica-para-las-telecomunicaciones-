"""Tests for forwarding logic."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from app.models.routing_table import RoutingTable
from app.services.forwarding_service import ForwardingService


class TestForwardingService(unittest.TestCase):
    def setUp(self):
        table = RoutingTable("R1")
        table.update_from_list([
            {"destination": "R3", "next_hop": "R2", "cost": 3},
        ])
        self.service = ForwardingService(table)

    def test_get_next_hop_known(self):
        self.assertEqual(self.service.get_next_hop("R3"), "R2")

    def test_get_next_hop_unknown(self):
        self.assertIsNone(self.service.get_next_hop("R99"))


if __name__ == "__main__":
    unittest.main()
