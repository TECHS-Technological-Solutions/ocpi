from uuid import uuid4

from py_ocpi.core.config import settings

from .utils import EMSP_BASE_URL, TARIFFS, AUTH_HEADERS, WRONG_AUTH_HEADERS


TARIFF_URL = (
    f"{EMSP_BASE_URL}{settings.COUNTRY_CODE}/{settings.PARTY_ID}/"
    f'{TARIFFS[0]["id"]}'
)


def test_emsp_get_tariff_not_authenticated(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.get(TARIFF_URL, headers=WRONG_AUTH_HEADERS)

    assert response.status_code == 403


def test_emsp_add_tariff_not_authenticated(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.put(
        TARIFF_URL,
        json=[0],
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_patch_tariff_not_authenticated(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.patch(
        TARIFF_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_delete_tariff_not_authenticated(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.delete(
        TARIFF_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_emsp_get_tariff_v_2_1_1(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.get(TARIFF_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == TARIFFS[0]["id"]


def test_emsp_add_tariff_v_2_1_1(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.put(
        TARIFF_URL,
        json=TARIFFS[0],
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == TARIFFS[0]["id"]


def test_emsp_patch_tariff_v_2_1_1(client_emsp_v_2_1_1):
    patch_data = {"id": str(uuid4())}
    response = client_emsp_v_2_1_1.patch(
        TARIFF_URL,
        json=patch_data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["id"] == patch_data["id"]


def test_emsp_delete_tariff_v_2_1_1(client_emsp_v_2_1_1):
    response = client_emsp_v_2_1_1.delete(TARIFF_URL, headers=AUTH_HEADERS)

    assert response.status_code == 200
