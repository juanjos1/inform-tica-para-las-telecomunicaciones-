"""Tests for FR-01: Router Registration."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import patch
from app.controllers.router_registry_controller import RouterRegistryController


class TestRouterRegistry(unittest.TestCase):
    def setUp(self):
        # Patch DAO so tests don't touch the filesystem
        patcher_load = patch("app.controllers.router_registry_controller.router_dao.load_routers", return_value={})
        patcher_save = patch("app.controllers.router_registry_controller.router_dao.save_routers")
        patcher_log  = patch("app.controllers.router_registry_controller.log_dao.append_log")
        self.mock_load = patcher_load.start()
        self.mock_save = patcher_save.start()
        self.mock_log  = patcher_log.start()
        self.addCleanup(patcher_load.stop)
        self.addCleanup(patcher_save.stop)
        self.addCleanup(patcher_log.stop)
        self.registry = RouterRegistryController()

    def test_register_stores_router(self):
        result = self.registry.register("R1", "127.0.0.1", 5001)
        self.assertTrue(result)
        self.assertIn("R1", self.registry.routers)

    def test_register_stores_correct_ip_port(self):
        self.registry.register("R2", "127.0.0.2", 5002)
        router = self.registry.get_router("R2")
        self.assertEqual(router.ip, "127.0.0.2")
        self.assertEqual(router.port, 5002)

    def test_register_multiple_routers(self):
        self.registry.register("R1", "127.0.0.1", 5001)
        self.registry.register("R2", "127.0.0.2", 5002)
        self.assertEqual(len(self.registry.all_routers()), 2)

    def test_register_duplicate_id_rejected(self):
        """Two different instances trying to use the same router_id (Error 1)."""
        first = self.registry.register("R1", "127.0.0.1", 5001)
        second = self.registry.register("R1", "10.0.0.5", 6000)
        self.assertTrue(first)
        self.assertFalse(second)
        # The original registration must be preserved, not overwritten
        router = self.registry.get_router("R1")
        self.assertEqual(router.ip, "127.0.0.1")
        self.assertEqual(router.port, 5001)
        self.assertEqual(len(self.registry.all_routers()), 1)

    def test_register_same_router_twice_rejected(self):
        """Same router sending REGISTER_ROUTER more than once (Error 2)."""
        first = self.registry.register("R1", "127.0.0.1", 5001)
        second = self.registry.register("R1", "127.0.0.1", 5001)
        self.assertTrue(first)
        self.assertFalse(second)

    def test_is_registered(self):
        self.assertFalse(self.registry.is_registered("R1"))
        self.registry.register("R1", "127.0.0.1", 5001)
        self.assertTrue(self.registry.is_registered("R1"))


if __name__ == "__main__":
    unittest.main()
