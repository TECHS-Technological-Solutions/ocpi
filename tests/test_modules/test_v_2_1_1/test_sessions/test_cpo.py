from .utils import CPO_BASE_URL, SESSIONS, AUTH_HEADERS, WRONG_AUTH_HEADERS

GET_SESSIONS_URL = CPO_BASE_URL


def test_cpo_get_sessions_not_authenticated(client_cpo_v_2_1_1):
    response = client_cpo_v_2_1_1.get(
        GET_SESSIONS_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_get_sessions_v_2_1_1(client_cpo_v_2_1_1):
    response = client_cpo_v_2_1_1.get(GET_SESSIONS_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["id"] == SESSIONS[0]["id"]
