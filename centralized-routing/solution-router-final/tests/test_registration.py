"""Tests for FR-01: Router registration (TC-01)."""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import unittest
from unittest.mock import MagicMock, patch
from app.services.registration_service import RegistrationService


class TestRegistration(unittest.TestCase):
    def setUp(self):
        self.conn = MagicMock()
        self.service = RegistrationService(self.conn)

    def test_register_sends_correct_message(self):
        self.conn.send.return_value = {"type": "ACK", "info": "registered"}
        with patch("app.services.registration_service.log_dao.append_log"):
            result = self.service.register("R1", "127.0.0.1", 5001)
        self.assertTrue(result)
        call_args = self.conn.send.call_args[0][0]
        self.assertEqual(call_args["type"], "REGISTER_ROUTER")
        self.assertEqual(call_args["router_id"], "R1")

    def test_register_fails_on_error_response(self):
        self.conn.send.return_value = {"type": "ERROR", "reason": "duplicate"}
        with patch("app.services.registration_service.log_dao.append_log"):
            result = self.service.register("R1", "127.0.0.1", 5001)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
