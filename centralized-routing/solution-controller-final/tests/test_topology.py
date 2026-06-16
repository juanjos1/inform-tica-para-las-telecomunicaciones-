"""Tests for FR-02, FR-03: Topology management."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from app.models.topology import Topology


class TestTopology(unittest.TestCase):
    def setUp(self):
        self.topology = Topology()

    def test_add_router(self):
        self.topology.add_router("R1")
        self.assertIn("R1", self.topology.graph)

    def test_update_neighbors_stores_links(self):
        neighbors = [{"neighbor_id": "R2", "cost": 10}, {"neighbor_id": "R3", "cost": 5}]
        self.topology.update_neighbors("R1", neighbors)
        self.assertIn(("R2", 10.0), self.topology.graph["R1"])
        self.assertIn(("R3", 5.0), self.topology.graph["R1"])

    def test_update_link_cost(self):
        self.topology.update_neighbors("R1", [{"neighbor_id": "R2", "cost": 10}])
        self.topology.update_link_cost("R1", "R2", 3)
        self.assertIn(("R2", 3), self.topology.graph["R1"])


if __name__ == "__main__":
    unittest.main()
