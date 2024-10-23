from .utils import (
    TOKEN_UPDATE,
    TOKENS,
    AUTH_HEADERS,
    WRONG_AUTH_HEADERS,
    CPO_BASE_URL,
)

TOKEN_URL = (
    f'{CPO_BASE_URL}{TOKENS[0]["country_code"]}/{TOKENS[0]["party_id"]}/'
    f'{TOKENS[0]["uid"]}'
)


def test_cpo_get_token_not_authenticated(client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.get(
        TOKEN_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_add_token_not_authenticated(client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.put(
        TOKEN_URL,
        json=TOKENS[0],
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_update_token_not_authenticated(client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.patch(
        TOKEN_URL,
        json=TOKEN_UPDATE,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_get_token_v_2_2_1(client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.get(
        TOKEN_URL,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == TOKENS[0]["uid"]


def test_cpo_add_token_v_2_2_1(client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.put(
        TOKEN_URL,
        json=TOKENS[0],
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == TOKENS[0]["uid"]


def test_cpo_update_token_v_2_2_1(client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.patch(
        TOKEN_URL,
        json=TOKEN_UPDATE,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert (
        response.json()["data"][0]["country_code"]
        == TOKEN_UPDATE["country_code"]
    )
