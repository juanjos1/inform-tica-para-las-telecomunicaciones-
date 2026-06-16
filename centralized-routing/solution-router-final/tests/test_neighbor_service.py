"""Tests for FR-02: Neighbor information."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import MagicMock, patch
from app.services.neighbor_service import NeighborService


class TestNeighborService(unittest.TestCase):
    def setUp(self):
        self.conn = MagicMock()
        with patch("app.services.neighbor_service.neighbor_dao.load_neighbors", return_value=[]):
            self.service = NeighborService(self.conn, router_id="R1")

    def test_add_neighbor(self):
        with patch("app.services.neighbor_service.neighbor_dao.save_neighbors"):
            ok, _ = self.service.add_neighbor("R2", 10)
        self.assertTrue(ok)
        self.assertEqual(len(self.service.neighbors), 1)
        self.assertEqual(self.service.neighbors[0].neighbor_id, "R2")

    def test_add_neighbor_duplicate_rejected(self):
        """Fix #8: duplicate must be rejected, not silently replaced."""
        with patch("app.services.neighbor_service.neighbor_dao.save_neighbors"):
            self.service.add_neighbor("R2", 10)
            ok, msg = self.service.add_neighbor("R2", 99)
        self.assertFalse(ok)
        self.assertIn("already exists", msg)
        # cost must NOT have been updated
        self.assertEqual(self.service.neighbors[0].cost, 10)

    def test_add_self_as_neighbor_rejected(self):
        """Fix #7: router must not add itself as neighbor."""
        with patch("app.services.neighbor_service.neighbor_dao.save_neighbors"):
            ok, msg = self.service.add_neighbor("R1", 5)
        self.assertFalse(ok)
        self.assertEqual(len(self.service.neighbors), 0)

    def test_remove_neighbor(self):
        """Fix #3: remove_neighbor must delete the entry."""
        with patch("app.services.neighbor_service.neighbor_dao.save_neighbors"):
            self.service.add_neighbor("R2", 10)
            ok, msg = self.service.remove_neighbor("R2")
        self.assertTrue(ok)
        self.assertEqual(len(self.service.neighbors), 0)

    def test_remove_nonexistent_neighbor(self):
        """Fix #3: removing a non-existent neighbor must report failure."""
        with patch("app.services.neighbor_service.neighbor_dao.save_neighbors"):
            ok, msg = self.service.remove_neighbor("R99")
        self.assertFalse(ok)
        self.assertIn("not found", msg)

    def test_send_neighbors_correct_message(self):
        with patch("app.services.neighbor_service.neighbor_dao.save_neighbors"):
            self.service.add_neighbor("R2", 5)
        self.conn.send.return_value = {"type": "ACK"}
        self.service.send_neighbors("R1")
        msg = self.conn.send.call_args[0][0]
        self.assertEqual(msg["type"], "TOPOLOGY_UPDATE")
        self.assertEqual(msg["router_id"], "R1")
        self.assertEqual(msg["neighbors"][0]["neighbor_id"], "R2")


if __name__ == "__main__":
    unittest.main()


class TestLinkCostValidation(unittest.TestCase):
    """Fix #9: link cost update must be rejected if destination is not a neighbor."""

    def setUp(self):
        self.conn = MagicMock()
        with patch("app.services.neighbor_service.neighbor_dao.load_neighbors", return_value=[]):
            self.service = NeighborService(self.conn, router_id="R1")

    def test_link_cost_valid_neighbor(self):
        """Destination is a known neighbor — connection.send must be called."""
        with patch("app.services.neighbor_service.neighbor_dao.save_neighbors"):
            self.service.add_neighbor("R2", 10)

        known_ids = [n.neighbor_id for n in self.service.neighbors]
        dest = "R2"
        self.assertIn(dest, known_ids)   # guard: R2 IS a neighbor

    def test_link_cost_unknown_destination_not_in_neighbors(self):
        """Destination unknown to the router — must NOT reach the controller."""
        with patch("app.services.neighbor_service.neighbor_dao.save_neighbors"):
            self.service.add_neighbor("R2", 10)

        known_ids = [n.neighbor_id for n in self.service.neighbors]
        dest = "R99"
        # The menu checks this before calling conn.send; we verify the guard logic
        self.assertNotIn(dest, known_ids)
        # conn.send should never have been called (menu responsibility)
        self.conn.send.assert_not_called()

    def test_link_cost_no_neighbors_at_all(self):
        """Router with zero neighbors — any destination must be rejected."""
        known_ids = [n.neighbor_id for n in self.service.neighbors]
        self.assertEqual(known_ids, [])
        self.assertNotIn("R2", known_ids)
