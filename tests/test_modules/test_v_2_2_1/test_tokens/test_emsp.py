from py_ocpi.modules.tokens.v_2_2_1.enums import AllowedType

from .utils import (
    EMSP_BASE_URL,
    TOKENS,
    AUTH_HEADERS,
    WRONG_AUTH_HEADERS,
)

GET_TOKEN = EMSP_BASE_URL
POST_TOKEN = f'{EMSP_BASE_URL}{TOKENS[0]["uid"]}/authorize'


def test_emsp_get_tokens_not_authenticated(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.get(GET_TOKEN, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_emsp_authorize_token_not_authenticated(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.post(POST_TOKEN, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_emsp_get_tokens_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.get(GET_TOKEN, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == TOKENS[0]["uid"]


def test_emsp_authorize_token_success_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.post(POST_TOKEN, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["allowed"] == AllowedType.allowed
