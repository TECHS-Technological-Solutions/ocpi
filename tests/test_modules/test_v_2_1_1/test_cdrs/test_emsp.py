from .utils import CDRS, AUTH_HEADERS, EMSP_BASE_URL, WRONG_AUTH_HEADERS

GET_CDR_URL = f'{EMSP_BASE_URL}{CDRS[0]["id"]}'
POST_CDR_URL = EMSP_BASE_URL


def test_emsp_get_cdr_not_authenticated(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.get(
        GET_CDR_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_add_cdr_not_authenticated(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.post(
        POST_CDR_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_get_cdr_v_2_1_1(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.get(GET_CDR_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == CDRS[0]["id"]


def test_emsp_add_cdr_v_2_1_1(client_emsp_v_2_1_1):
    data = CDRS[0]
    response = client_emsp_v_2_1_1.post(
        POST_CDR_URL,
        json=data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == CDRS[0]["id"]
    assert response.headers["Location"] is not None
