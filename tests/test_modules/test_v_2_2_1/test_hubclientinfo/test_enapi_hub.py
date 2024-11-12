import pytest
from unittest.mock import patch
from py_ocpi.modules.hubclientinfo.utils import HubTopologyHandler


@pytest.fixture
def handler():
    return HubTopologyHandler(
        hub_url="https://hub.enapi.com/ocpi",
        party_id="TEST_PARTY_ID",
        country_code="US",
        token="test_token"
    )


@patch('requests.post')
def test_register_with_hub_success(mock_post, handler):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "success"}

    response = handler.register_with_hub()
    assert response is not None
    assert response["status"] == "success"
    mock_post.assert_called_once_with(
        f"{handler.hub_url}/register",
        json={"party_id": handler.party_id, "country_code": handler.country_code},
        headers=handler.headers,
        timeout=30
    )


@patch('requests.post')
def test_register_with_hub_failure(mock_post, handler):
    mock_post.return_value.status_code = 400

    response = handler.register_with_hub()
    assert response is None
    mock_post.assert_called_once()


@patch('requests.post')
def test_route_message_success(mock_post, handler):
    mock_post.return_value.status_code = 200
    mock_post.return_value.json.return_value = {"status": "message routed"}

    response = handler.route_message("some_endpoint", {"key": "value"})
    assert response is not None
    assert response["status"] == "message routed"
    mock_post.assert_called_once_with(
        f"{handler.hub_url}/some_endpoint",
        json={"key": "value"},
        headers=handler.headers,
        timeout=30
    )


@patch('requests.post')
def test_route_message_failure(mock_post, handler):
    mock_post.return_value.status_code = 500

    response = handler.route_message("some_endpoint", {"key": "value"})
    assert response is None
    mock_post.assert_called_once()


def test_handle_incoming_message_command(handler):
    payload = {"type": "COMMAND", "command": "START_SESSION", "session_id": "12345"}
    response = handler.handle_incoming_message(payload)
    assert response["status"] == "Session 12345 started successfully"


def test_handle_incoming_message_unknown_type(handler):
    payload = {"type": "UNKNOWN"}
    response = handler.handle_incoming_message(payload)
    assert response["status"] == "Unknown message type"


def test_process_command_start_session(handler):
    payload = {"command": "START_SESSION", "session_id": "12345"}
    response = handler.process_command(payload)
    assert response["status"] == "Session 12345 started successfully"


def test_process_command_stop_session(handler):
    payload = {"command": "STOP_SESSION", "session_id": "54321"}
    response = handler.process_command(payload)
    assert response["status"] == "Session 54321 stopped successfully"


def test_process_command_unknown_command(handler):
    payload = {"command": "INVALID_COMMAND"}
    response = handler.process_command(payload)
    assert response["status"] == "Unknown command"