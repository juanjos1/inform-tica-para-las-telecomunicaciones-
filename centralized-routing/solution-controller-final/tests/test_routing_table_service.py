"""Tests for FR-05: Routing table generation."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from app.models.topology import Topology
from app.services.routing_table_service import build_all_routing_tables


class TestRoutingTableService(unittest.TestCase):
    def setUp(self):
        self.topology = Topology()
        self.topology.update_neighbors("R1", [{"neighbor_id": "R2", "cost": 2}, {"neighbor_id": "R3", "cost": 5}])
        self.topology.update_neighbors("R2", [{"neighbor_id": "R1", "cost": 2}, {"neighbor_id": "R3", "cost": 1}])
        self.topology.update_neighbors("R3", [{"neighbor_id": "R2", "cost": 1}, {"neighbor_id": "R1", "cost": 5}])

    def test_tables_generated_for_all_routers(self):
        tables = build_all_routing_tables(self.topology)
        self.assertIn("R1", tables)
        self.assertIn("R2", tables)
        self.assertIn("R3", tables)

    def test_r1_table_has_correct_next_hop_to_r3(self):
        """R1 -> R3 should use R2 as next hop."""
        tables = build_all_routing_tables(self.topology)
        r1_table = tables["R1"]
        entry_to_r3 = next(e for e in r1_table.entries if e.destination == "R3")
        self.assertEqual(entry_to_r3.next_hop, "R2")
        self.assertEqual(entry_to_r3.cost, 3.0)


if __name__ == "__main__":
    unittest.main()
