from .utils import (
    CHARGING_PREFERENCES,
    SESSIONS,
    AUTH_HEADERS,
    WRONG_AUTH_HEADERS,
    CPO_BASE_URL,
)

GET_SESSION_URL = CPO_BASE_URL
PUT_SESSION_URL = f'{CPO_BASE_URL}{SESSIONS[0]["id"]}/charging_preferences'


def test_cpo_get_sessions_not_authenticated(client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.get(
        GET_SESSION_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_set_charging_preference_not_authenticated(client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.put(
        PUT_SESSION_URL,
        json=CHARGING_PREFERENCES,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_get_sessions_v_2_2_1(client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.get(GET_SESSION_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["id"] == SESSIONS[0]["id"]


def test_cpo_set_charging_preference_v_2_2_1(client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.put(
        PUT_SESSION_URL,
        json=CHARGING_PREFERENCES,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert (
        response.json()["data"][0]["energy_need"]
        == CHARGING_PREFERENCES["energy_need"]
    )
