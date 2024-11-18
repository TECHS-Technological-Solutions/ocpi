from .utils import (
    COMMAND_RESPONSE,
    EMSP_BASE_URL,
    AUTH_HEADERS,
    WRONG_AUTH_HEADERS,
)

RECEIVE_URL = f"{EMSP_BASE_URL}1234"


def test_emsp_receive_command_result_not_authenticated(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.post(
        RECEIVE_URL,
        json=COMMAND_RESPONSE,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_receive_command_result_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.post(
        RECEIVE_URL,
        json=COMMAND_RESPONSE,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
