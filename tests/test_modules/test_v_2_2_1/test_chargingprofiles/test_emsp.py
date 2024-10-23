from .utils import (
    CHARGING_PROFILE,
    EMSP_BASE_URL,
    AUTH_HEADERS,
    WRONG_AUTH_HEADERS,
)

RECEIVE_URL = f"{EMSP_BASE_URL}"
ADD_OR_UPDATE_URL = f"{EMSP_BASE_URL}1234"


def test_emsp_receive_chargingprofile_result_not_authenticated(
    client_emsp_v_2_2_1,
):
    response = client_emsp_v_2_2_1.post(
        RECEIVE_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_add_or_update_not_authenticated(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.put(
        ADD_OR_UPDATE_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_receive_chargingprofile_result_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.post(
        RECEIVE_URL,
        json={},
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200


def test_emsp_add_or_update_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.put(
        ADD_OR_UPDATE_URL,
        json=CHARGING_PROFILE,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
