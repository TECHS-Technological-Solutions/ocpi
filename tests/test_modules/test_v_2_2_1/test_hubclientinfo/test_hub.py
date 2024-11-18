import unittest
from unittest.mock import patch
from py_ocpi.modules.hubclientinfo.utils import HubTopologyHandler


class TestHubTopologyHandler(unittest.TestCase):
    def setUp(self):
        self.hub_handler = HubTopologyHandler(
            hub_url="https://example-hub.com",
            party_id="ESMP",
            country_code="NL",
            token="sample_token"
        )

    @patch("py_ocpi.modules.hubclientinfo.utils.requests.post")
    def test_register_with_hub_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "registered"}

        result = self.hub_handler.register_with_hub()
        self.assertEqual(result["status"], "registered")

    @patch("py_ocpi.modules.hubclientinfo.utils.requests.post")
    def test_register_with_hub_failure(self, mock_post):
        mock_post.return_value.status_code = 400

        result = self.hub_handler.register_with_hub()
        self.assertIsNone(result)

    @patch("py_ocpi.modules.hubclientinfo.utils.requests.post")
    def test_route_message_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"status": "message routed"}

        payload = {"data": "test"}
        result = self.hub_handler.route_message("test_endpoint", payload)
        self.assertEqual(result["status"], "message routed")

    @patch("py_ocpi.modules.hubclientinfo.utils.requests.post")
    def test_route_message_failure(self, mock_post):
        mock_post.return_value.status_code = 400

        payload = {"data": "test"}
        result = self.hub_handler.route_message("test_endpoint", payload)
        self.assertIsNone(result)

    def test_handle_incoming_message_command(self):
        payload = {"type": "COMMAND", "command": "START_SESSION", "session_id": "123"}
        result = self.hub_handler.handle_incoming_message(payload)
        self.assertEqual(result["status"], "Session 123 started successfully")

    def test_handle_incoming_message_unknown_type(self):
        payload = {"type": "UNKNOWN"}
        result = self.hub_handler.handle_incoming_message(payload)
        self.assertEqual(result["status"], "Unknown message type")

    def test_process_command_start_session(self):
        payload = {"command": "START_SESSION", "session_id": "123"}
        result = self.hub_handler.process_command(payload)
        self.assertEqual(result["status"], "Session 123 started successfully")

    def test_process_command_stop_session(self):
        payload = {"command": "STOP_SESSION", "session_id": "123"}
        result = self.hub_handler.process_command(payload)
        self.assertEqual(result["status"], "Session 123 stopped successfully")

    def test_process_command_unknown(self):
        payload = {"command": "UNKNOWN_COMMAND"}
        result = self.hub_handler.process_command(payload)
        self.assertEqual(result["status"], "Unknown command")
