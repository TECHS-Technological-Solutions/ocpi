from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi import get_application
from py_ocpi.core import enums
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.modules.tokens.v_2_2_1.enums import TokenType, WhitelistType
from py_ocpi.modules.commands.v_2_2_1.enums import CommandType, CommandResponseType, CommandResultType
from py_ocpi.modules.commands.v_2_2_1.schemas import CommandResponse, CommandResult
from py_ocpi.modules.versions.enums import VersionNumber

COMMAND_RESPONSE = {
    'result': CommandResponseType.accepted,
    'timeout': 30
}

COMMAND_RESULT = {
    'result': CommandResultType.accepted,
}


class Crud:

    @classmethod
    async def do(cls, module: enums.ModuleID, role: enums.RoleEnum, action: enums.Action,
                 *args, data: dict = None, **kwargs) -> dict:
        return COMMAND_RESPONSE

    @classmethod
    async def get(cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs) -> dict:
        return COMMAND_RESULT

    @classmethod
    async def update(cls, module: enums.ModuleID, role: enums.RoleEnum, data: dict, id, *args, **kwargs):
        ...


class Adapter:
    @classmethod
    def command_response_adapter(cls, data, version: VersionNumber = VersionNumber.latest):
        return CommandResponse(**data)

    @classmethod
    def command_result_adapter(cls, data, version: VersionNumber = VersionNumber.latest):
        return CommandResult(**data)


def test_cpo_receive_command_start_session_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    data = {
        'response_url': 'https://dummy.restapiexample.com/api/v1/create',
        'token': {
            'country_code': 'us',
            'party_id': 'AAA',
            'uid': str(uuid4()),
            'type': TokenType.rfid,
            'contract_id': str(uuid4()),
            'issuer': 'company',
            'valid': True,
            'whitelist': WhitelistType.always,
            'last_updated': '2022-01-02 00:00:00+00:00'

        },
        'location_id': str(uuid4())
    }

    client = TestClient(app)
    response = client.post(f'/ocpi/cpo/2.2.1/commands/{CommandType.start_session}', json=data)

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['result'] == COMMAND_RESPONSE["result"]


def test_cpo_receive_command_stop_session_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    data = {
        'response_url': 'https://dummy.restapiexample.com/api/v1/create',
        'session_id': str(uuid4())
    }

    client = TestClient(app)
    response = client.post(f'/ocpi/cpo/2.2.1/commands/{CommandType.stop_session}', json=data)

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['result'] == COMMAND_RESPONSE["result"]


def test_cpo_receive_command_reserve_now_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    data = {
        'response_url': 'https://dummy.restapiexample.com/api/v1/create',
        'token': {
            'country_code': 'us',
            'party_id': 'AAA',
            'uid': str(uuid4()),
            'type': TokenType.rfid,
            'contract_id': str(uuid4()),
            'issuer': 'company',
            'valid': True,
            'whitelist': WhitelistType.always,
            'last_updated': '2022-01-02 00:00:00+00:00'

        },
        'expiry_date': str(datetime.datetime.now() + datetime.timedelta(days=1)),
        'reservation_id': str(uuid4()),
        'location_id': str(uuid4())
    }

    client = TestClient(app)
    response = client.post(f'/ocpi/cpo/2.2.1/commands/{CommandType.reserve_now}', json=data)

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['result'] == COMMAND_RESPONSE["result"]


def test_cpo_receive_command_reserve_now_unknown_location_v_2_2_1():

    @classmethod
    async def get(cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs) -> dict:
        if module == enums.ModuleID.commands:
            return COMMAND_RESULT
        if module == enums.ModuleID.locations:
            raise NotFoundOCPIError()
    _get = Crud.get
    Crud.get = get

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    data = {
        'response_url': 'https://dummy.restapiexample.com/api/v1/create',
        'token': {
            'country_code': 'us',
            'party_id': 'AAA',
            'uid': str(uuid4()),
            'type': TokenType.rfid,
            'contract_id': str(uuid4()),
            'issuer': 'company',
            'valid': True,
            'whitelist': WhitelistType.always,
            'last_updated': '2022-01-02 00:00:00+00:00'

        },
        'expiry_date': str(datetime.datetime.now() + datetime.timedelta(days=1)),
        'reservation_id': str(uuid4()),
        'location_id': str(uuid4())
    }

    client = TestClient(app)
    response = client.post(f'/ocpi/cpo/2.2.1/commands/{CommandType.reserve_now}', json=data)

    assert response.status_code == 200
    assert response.json()['data'][0]['result'] == CommandResultType.rejected

    # revert Crud changes
    Crud.get = _get


def test_emsp_receive_command_result_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.post('/ocpi/emsp/2.2.1/commands/1234', json=COMMAND_RESPONSE)

    assert response.status_code == 200
