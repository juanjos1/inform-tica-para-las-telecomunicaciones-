"""Tests for FR-06: Routing table storage."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import patch
from app.services.routing_table_service import RoutingTableService


class TestRoutingTableStorage(unittest.TestCase):
    def setUp(self):
        self.service = RoutingTableService("R1")

    def test_update_routing_table(self):
        entries = [
            {"destination": "R2", "next_hop": "R2", "cost": 5},
            {"destination": "R3", "next_hop": "R2", "cost": 8},
        ]
        with patch("app.services.routing_table_service.routing_table_dao.save_routing_table"):
            self.service.update(entries)
        table = self.service.get_table()
        self.assertEqual(len(table.entries), 2)
        self.assertEqual(table.entries[0].destination, "R2")


if __name__ == "__main__":
    unittest.main()
