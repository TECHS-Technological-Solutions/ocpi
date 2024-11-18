import pytest

import datetime
from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi import get_application
from py_ocpi.core import enums
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.modules.commands.v_2_1_1.enums import (
    CommandType,
    CommandResponseType,
)
from py_ocpi.modules.versions.enums import VersionNumber

from .utils import (
    Crud,
    ClientAuthenticator,
    COMMAND_RESPONSE,
    CPO_BASE_URL,
    AUTH_HEADERS,
    WRONG_AUTH_HEADERS,
)

from tests.test_modules.test_v_2_1_1.test_tokens.utils import TOKENS

COMMAND_START_URL = f"{CPO_BASE_URL}{CommandType.start_session.value}"
COMMAND_STOP_URL = f"{CPO_BASE_URL}{CommandType.stop_session.value}"
RESERVE_NOW_URL = f"{CPO_BASE_URL}{CommandType.reserve_now.value}"


@pytest.mark.parametrize(
    "endpoint",
    [
        COMMAND_START_URL,
        COMMAND_STOP_URL,
        RESERVE_NOW_URL,
    ],
)
def test_cpo_receive_command_start_session_not_authenticated(
    client_cpo_v_2_1_1,
    endpoint,
):
    response = client_cpo_v_2_1_1.post(
        endpoint,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 403


def test_cpo_receive_command_start_session_v_2_1_1(client_cpo_v_2_1_1):
    data = {
        "response_url": "https://dummy.restapiexample.com/api/v1/create",
        "token": TOKENS[0],
        "location_id": str(uuid4()),
    }

    response = client_cpo_v_2_1_1.post(
        COMMAND_START_URL,
        json=data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["result"] == COMMAND_RESPONSE["result"]


def test_cpo_receive_command_stop_session_v_2_1_1(client_cpo_v_2_1_1):
    data = {
        "response_url": "https://dummy.restapiexample.com/api/v1/create",
        "session_id": str(uuid4()),
    }

    response = client_cpo_v_2_1_1.post(
        COMMAND_STOP_URL,
        json=data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["result"] == COMMAND_RESPONSE["result"]


def test_cpo_receive_command_reserve_now_v_2_1_1(client_cpo_v_2_1_1):
    data = {
        "response_url": "https://dummy.restapiexample.com/api/v1/create",
        "token": TOKENS[0],
        "expiry_date": str(
            datetime.datetime.now() + datetime.timedelta(days=1)
        ),
        "reservation_id": 0,
        "location_id": str(uuid4()),
    }

    response = client_cpo_v_2_1_1.post(
        RESERVE_NOW_URL,
        json=data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1
    assert response.json()["data"][0]["result"] == COMMAND_RESPONSE["result"]


def test_cpo_receive_command_reserve_now_unknown_location_v_2_1_1():
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ) -> dict:
        if module == enums.ModuleID.commands:
            return COMMAND_RESPONSE
        if module == enums.ModuleID.locations:
            raise NotFoundOCPIError()

    _get = Crud.get
    Crud.get = get

    app = get_application(
        version_numbers=[VersionNumber.v_2_1_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.commands],
    )

    data = {
        "response_url": "https://dummy.restapiexample.com/api/v1/create",
        "token": TOKENS[0],
        "expiry_date": str(
            datetime.datetime.now() + datetime.timedelta(days=1)
        ),
        "reservation_id": 0,
        "location_id": str(uuid4()),
    }

    client = TestClient(app)
    response = client.post(
        RESERVE_NOW_URL,
        json=data,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert response.json()["data"][0]["result"] == CommandResponseType.rejected

    # revert Crud changes
    Crud.get = _get
