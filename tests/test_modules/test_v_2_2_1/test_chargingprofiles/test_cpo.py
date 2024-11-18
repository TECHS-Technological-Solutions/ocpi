from unittest.mock import patch

from py_ocpi.modules.chargingprofiles.v_2_2_1.schemas import (
    ChargingProfileResponseType,
)

from .utils import (
    CPO_BASE_URL,
    AUTH_HEADERS,
    WRONG_AUTH_HEADERS,
    SET_CHARGING_PROFILE,
)

CHARGINGPROFILE_URL = f"{CPO_BASE_URL}1234"


def test_cpo_get_chargingprofile_not_authenticated(client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.get(
        CHARGINGPROFILE_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_add_or_update_chargingprofile_not_authenticated(
    client_cpo_v_2_2_1,
):
    response = client_cpo_v_2_2_1.put(
        CHARGINGPROFILE_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_delete_chargingprofile_not_authenticated(client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.delete(
        CHARGINGPROFILE_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


@patch("tests.test_modules.test_v_2_2_1.test_chargingprofiles.utils.Crud.get")
def test_cpo_get_chargingprofile_no_session(mock_get, client_cpo_v_2_2_1):
    mock_get.return_value = None

    response = client_cpo_v_2_2_1.get(
        f"{CHARGINGPROFILE_URL}?duration={1}&response_url=abs",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert (
        response.json()["data"][0]["result"]
        == ChargingProfileResponseType.rejected
    )


@patch("tests.test_modules.test_v_2_2_1.test_chargingprofiles.utils.Crud.do")
def test_cpo_get_chargingprofile_no_charging_response(
    mock_do, client_cpo_v_2_2_1
):
    mock_do.return_value = None

    response = client_cpo_v_2_2_1.get(
        f"{CHARGINGPROFILE_URL}?duration={1}&response_url=abs",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert (
        response.json()["data"][0]["result"]
        == ChargingProfileResponseType.rejected
    )


@patch(
    "py_ocpi.modules.chargingprofiles.v_2_2_1.api.cpo.BackgroundTasks.add_task"
)
def test_cpo_get_chargingprofile_v_2_2_1(mock_background, client_cpo_v_2_2_1):
    response = client_cpo_v_2_2_1.get(
        f"{CHARGINGPROFILE_URL}?duration={1}&response_url=abs",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert (
        response.json()["data"][0]["result"]
        == ChargingProfileResponseType.accepted
    )
    assert mock_background.call_count == 1


@patch("tests.test_modules.test_v_2_2_1.test_chargingprofiles.utils.Crud.get")
def test_cpo_add_or_update_chargingprofile_no_session(
    mock_get, client_cpo_v_2_2_1
):
    mock_get.return_value = None

    response = client_cpo_v_2_2_1.put(
        CHARGINGPROFILE_URL,
        json=SET_CHARGING_PROFILE,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert (
        response.json()["data"][0]["result"]
        == ChargingProfileResponseType.rejected
    )


@patch("tests.test_modules.test_v_2_2_1.test_chargingprofiles.utils.Crud.do")
def test_cpo_add_or_update_chargingprofile_no_charging_response(
    mock_do, client_cpo_v_2_2_1
):
    mock_do.return_value = None

    response = client_cpo_v_2_2_1.put(
        CHARGINGPROFILE_URL,
        json=SET_CHARGING_PROFILE,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert (
        response.json()["data"][0]["result"]
        == ChargingProfileResponseType.rejected
    )


@patch(
    "py_ocpi.modules.chargingprofiles.v_2_2_1.api.cpo.BackgroundTasks.add_task"
)
def test_cpo_add_or_update_chargingprofile_v_2_2_1(
    mock_background, client_cpo_v_2_2_1
):
    response = client_cpo_v_2_2_1.put(
        CHARGINGPROFILE_URL,
        json=SET_CHARGING_PROFILE,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert (
        response.json()["data"][0]["result"]
        == ChargingProfileResponseType.accepted
    )
    assert mock_background.call_count == 1


@patch("tests.test_modules.test_v_2_2_1.test_chargingprofiles.utils.Crud.get")
def test_cpo_delete_chargingprofile_no_session(mock_get, client_cpo_v_2_2_1):
    mock_get.return_value = None

    response = client_cpo_v_2_2_1.delete(
        f"{CHARGINGPROFILE_URL}?response_url=abs",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert (
        response.json()["data"][0]["result"]
        == ChargingProfileResponseType.rejected
    )


@patch("tests.test_modules.test_v_2_2_1.test_chargingprofiles.utils.Crud.do")
def test_cpo_delete_chargingprofile_no_charging_response(
    mock_do, client_cpo_v_2_2_1
):
    mock_do.return_value = None

    response = client_cpo_v_2_2_1.delete(
        f"{CHARGINGPROFILE_URL}?response_url=abs",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert (
        response.json()["data"][0]["result"]
        == ChargingProfileResponseType.rejected
    )


@patch(
    "py_ocpi.modules.chargingprofiles.v_2_2_1.api.cpo.BackgroundTasks.add_task"
)
def test_cpo_delete_chargingprofile_v_2_2_1(
    mock_background, client_cpo_v_2_2_1
):
    response = client_cpo_v_2_2_1.delete(
        f"{CHARGINGPROFILE_URL}?response_url=abs",
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert (
        response.json()["data"][0]["result"]
        == ChargingProfileResponseType.accepted
    )
    assert mock_background.call_count == 1
