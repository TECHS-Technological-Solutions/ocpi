import pytest

from uuid import uuid4

from py_ocpi.core.config import settings

from .utils import EMSP_BASE_URL, AUTH_HEADERS, LOCATIONS, WRONG_AUTH_HEADERS

LOCATION_URL = (
    f"{EMSP_BASE_URL}{settings.COUNTRY_CODE}/{settings.PARTY_ID}/"
    f"{LOCATIONS[0]['id']}"
)
EVSE_URL = (
    f"{EMSP_BASE_URL}{settings.COUNTRY_CODE}/{settings.PARTY_ID}/"
    f"{LOCATIONS[0]['id']}/{LOCATIONS[0]['evses'][0]['uid']}"
)
CONNECTOR_URL = (
    f"{EMSP_BASE_URL}{settings.COUNTRY_CODE}/{settings.PARTY_ID}/"
    f'{LOCATIONS[0]["id"]}/{LOCATIONS[0]["evses"][0]["uid"]}/'
    f'{LOCATIONS[0]["evses"][0]["connectors"][0]["id"]}'
)


@pytest.mark.parametrize(
    "endpoint",
    [
        LOCATION_URL,
        EVSE_URL,
        CONNECTOR_URL,
    ],
)
def test_emsp_get_locations_not_authenticated(client_emsp_v_2_2_1, endpoint):
    response = client_emsp_v_2_2_1.get(
        url=endpoint,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


@pytest.mark.parametrize(
    "endpoint",
    [
        LOCATION_URL,
        EVSE_URL,
        CONNECTOR_URL,
    ],
)
def test_emsp_put_locations_not_authenticated(client_emsp_v_2_2_1, endpoint):
    response = client_emsp_v_2_2_1.put(
        url=endpoint,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


@pytest.mark.parametrize(
    "endpoint",
    [
        LOCATION_URL,
        EVSE_URL,
        CONNECTOR_URL,
    ],
)
def test_emsp_patch_locations_not_authenticated(client_emsp_v_2_2_1, endpoint):
    response = client_emsp_v_2_2_1.patch(
        url=endpoint,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_get_location_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.get(LOCATION_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == LOCATIONS[0]["id"]


def test_emsp_get_evse_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.get(EVSE_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == LOCATIONS[0]["evses"][0]["uid"]


def test_emsp_get_connector_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.get(CONNECTOR_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert (
        response.json()["data"][0]["id"]
        == LOCATIONS[0]["evses"][0]["connectors"][0]["id"]
    )


def test_emsp_add_location_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.put(
        LOCATION_URL,
        json=LOCATIONS[0],
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == LOCATIONS[0]["id"]


def test_emsp_add_evse_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.put(
        EVSE_URL,
        json=LOCATIONS[0]["evses"][0],
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == LOCATIONS[0]["evses"][0]["uid"]


def test_emsp_add_connector_v_2_2_1(client_emsp_v_2_2_1):
    response = client_emsp_v_2_2_1.put(
        CONNECTOR_URL,
        json=LOCATIONS[0]["evses"][0]["connectors"][0],
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert (
        response.json()["data"][0]["id"]
        == LOCATIONS[0]["evses"][0]["connectors"][0]["id"]
    )


def test_emsp_patch_location_v_2_2_1(client_emsp_v_2_2_1):
    patch_data = {"id": str(uuid4())}
    response = client_emsp_v_2_2_1.patch(
        LOCATION_URL,
        json=patch_data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == patch_data["id"]


def test_emsp_patch_evse_v_2_2_1(client_emsp_v_2_2_1):
    patch_data = {"uid": str(uuid4())}
    response = client_emsp_v_2_2_1.patch(
        EVSE_URL,
        json=patch_data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["uid"] == patch_data["uid"]


def test_emsp_patch_connector_v_2_2_1(client_emsp_v_2_2_1):
    patch_data = {"id": str(uuid4())}
    response = client_emsp_v_2_2_1.patch(
        CONNECTOR_URL,
        json=patch_data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["id"] == patch_data["id"]
