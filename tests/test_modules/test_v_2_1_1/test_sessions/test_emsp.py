from uuid import uuid4

from py_ocpi.core.config import settings

from .utils import EMSP_BASE_URL, SESSIONS, AUTH_HEADERS, WRONG_AUTH_HEADERS

GET_SESSION = (
    f"{EMSP_BASE_URL}{settings.COUNTRY_CODE}/{settings.PARTY_ID}/"
    f'{SESSIONS[0]["id"]}'
)


def test_emsp_get_session_not_authenticated(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.get(GET_SESSION, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_emsp_add_session_not_authenticated(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.put(
        GET_SESSION,
        json=SESSIONS[0],
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_patch_session_not_authenticated(client_emsp_v_2_1_1):
    patch_data = {"id": str(uuid4())}
    response = client_emsp_v_2_1_1.patch(
        GET_SESSION,
        json=patch_data,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_get_session_v_2_1_1(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.get(GET_SESSION, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == SESSIONS[0]["id"]


def test_emsp_add_session_v_2_1_1(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.put(
        GET_SESSION,
        json=SESSIONS[0],
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == SESSIONS[0]["id"]


def test_emsp_patch_session_v_2_1_1(client_emsp_v_2_1_1):
    patch_data = {"id": str(uuid4())}
    response = client_emsp_v_2_1_1.patch(
        GET_SESSION,
        json=patch_data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == patch_data["id"]
