"""Tests for FR-04: Dijkstra shortest path."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from app.models.topology import Topology
from app.services.dijkstra_service import dijkstra


class TestDijkstra(unittest.TestCase):
    def setUp(self):
        self.topology = Topology()
        # R1-R2 cost 2, R2-R3 cost 1, R1-R3 cost 5
        self.topology.update_neighbors("R1", [{"neighbor_id": "R2", "cost": 2}, {"neighbor_id": "R3", "cost": 5}])
        self.topology.update_neighbors("R2", [{"neighbor_id": "R1", "cost": 2}, {"neighbor_id": "R3", "cost": 1}])
        self.topology.update_neighbors("R3", [{"neighbor_id": "R2", "cost": 1}, {"neighbor_id": "R1", "cost": 5}])

    def test_shortest_path_r1_to_r3(self):
        """TC-03: shortest path R1->R3 should be R1->R2->R3 cost 3."""
        result = dijkstra(self.topology, "R1")
        cost, path = result["R3"]
        self.assertEqual(cost, 3.0)
        self.assertEqual(path, ["R1", "R2", "R3"])

    def test_shortest_path_r1_to_r2(self):
        result = dijkstra(self.topology, "R1")
        cost, path = result["R2"]
        self.assertEqual(cost, 2.0)

    def test_all_nodes_reachable(self):
        result = dijkstra(self.topology, "R1")
        self.assertIn("R2", result)
        self.assertIn("R3", result)


if __name__ == "__main__":
    unittest.main()
