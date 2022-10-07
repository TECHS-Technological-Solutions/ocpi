from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi.core import enums
from py_ocpi.tokens.v_2_2_1.enums import TokenType, WhitelistType
from py_ocpi.commands.v_2_2_1.enums import CommandType, CommandResponseType
from py_ocpi.commands.v_2_2_1.schemas import CommandResponse
from py_ocpi.main import get_application
from py_ocpi.versions.enums import VersionNumber

COMMAND_RESPONSE = {
    'result': CommandResponseType.accepted,
    'timeout': 30
}


class Crud:

    @classmethod
    async def create(cls, module: enums.ModuleID, filters: dict, *args, **kwargs) -> dict:
        return COMMAND_RESPONSE


class Adapter:
    @classmethod
    def commands_adapter(cls, data) -> CommandResponse:
        return CommandResponse(**data)


def test_receive_command():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    data = {
        'response_url': 'https://www.w3.org/Addressing/URL/uri-spec.html',
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