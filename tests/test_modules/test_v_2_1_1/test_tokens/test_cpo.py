from py_ocpi.core.config import settings

from .utils import (
    TOKENS,
    TOKEN_UPDATE,
    CPO_BASE_URL,
    AUTH_HEADERS,
    WRONG_AUTH_HEADERS,
)

TOKEN_URL = (
    f"{CPO_BASE_URL}{settings.COUNTRY_CODE}/{settings.PARTY_ID}/"
    f'{TOKENS[0]["uid"]}'
)


def test_cpo_get_token_not_authenticated(client_cpo_v_2_1_1):
    response = client_cpo_v_2_1_1.get(TOKEN_URL, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_cpo_add_token_not_authenticate(client_cpo_v_2_1_1):
    response = client_cpo_v_2_1_1.put(
        TOKEN_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_update_token_not_authenticate(client_cpo_v_2_1_1):
    response = client_cpo_v_2_1_1.patch(
        TOKEN_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_get_token_v_2_1_1(client_cpo_v_2_1_1):
    response = client_cpo_v_2_1_1.get(TOKEN_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == TOKENS[0]["uid"]


def test_cpo_add_token_v_2_1_1(client_cpo_v_2_1_1):
    response = client_cpo_v_2_1_1.put(
        TOKEN_URL,
        json=TOKENS[0],
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == TOKENS[0]["uid"]


def test_cpo_update_token_v_2_1_1(client_cpo_v_2_1_1):
    response = client_cpo_v_2_1_1.patch(
        TOKEN_URL,
        json=TOKEN_UPDATE,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["valid"] == TOKEN_UPDATE["valid"]
