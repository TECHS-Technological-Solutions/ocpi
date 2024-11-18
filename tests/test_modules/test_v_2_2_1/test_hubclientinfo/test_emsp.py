from py_ocpi.core.config import settings

from .utils import CLIENT_INFO, AUTH_HEADERS, WRONG_AUTH_HEADERS, EMSP_BASE_URL

CLIENT_INFO_URL = f"{EMSP_BASE_URL}{settings.COUNTRY_CODE}/{settings.PARTY_ID}"


def test_cpo_get_clientinfo_not_authenticated(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.get(
        CLIENT_INFO_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_put_clientinfo_not_authenticated(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.put(
        CLIENT_INFO_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_get_clientinfo_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.get(CLIENT_INFO_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0] == CLIENT_INFO[0]


def test_cpo_add_clientinfo_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.put(
        CLIENT_INFO_URL,
        headers=AUTH_HEADERS,
        json=CLIENT_INFO[0],
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0] == CLIENT_INFO[0]
