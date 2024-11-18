import pytest

from .utils import CPO_BASE_URL, AUTH_HEADERS, LOCATIONS, WRONG_AUTH_HEADERS

GET_LOCATIONS_URL = CPO_BASE_URL
GET_LOCATION_URL = f'{CPO_BASE_URL}{LOCATIONS[0]["id"]}'
GET_EVSE_URL = (
    f'{CPO_BASE_URL}{LOCATIONS[0]["id"]}' f'/{LOCATIONS[0]["evses"][0]["uid"]}'
)
GET_CONNECTOR_URL = (
    f'{CPO_BASE_URL}{LOCATIONS[0]["id"]}'
    f'/{LOCATIONS[0]["evses"][0]["uid"]}'
    f'/{LOCATIONS[0]["evses"][0]["connectors"][0]["id"]}'
)


@pytest.mark.parametrize(
    "endpoint",
    [
        GET_LOCATIONS_URL,
        GET_LOCATION_URL,
        GET_EVSE_URL,
        GET_CONNECTOR_URL,
    ],
)
def test_cpo_locations_not_authenticated(client_cpo_v_2_1_1, endpoint):
    response = client_cpo_v_2_1_1.get(endpoint, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_cpo_get_locations_v_2_1_1(client_cpo_v_2_1_1):
    response = client_cpo_v_2_1_1.get(GET_LOCATIONS_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["id"] == LOCATIONS[0]["id"]


def test_cpo_get_location_v_2_1_1(client_cpo_v_2_1_1):
    response = client_cpo_v_2_1_1.get(GET_LOCATION_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == LOCATIONS[0]["id"]


def test_cpo_get_evse_v_2_1_1(client_cpo_v_2_1_1):
    response = client_cpo_v_2_1_1.get(GET_EVSE_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == LOCATIONS[0]["evses"][0]["uid"]


def test_cpo_get_connector_v_2_1_1(client_cpo_v_2_1_1):
    response = client_cpo_v_2_1_1.get(GET_CONNECTOR_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert (
        response.json()["data"][0]["id"]
        == LOCATIONS[0]["evses"][0]["connectors"][0]["id"]
    )
