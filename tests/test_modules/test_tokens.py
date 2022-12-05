from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi.main import get_application
from py_ocpi.core import enums
from py_ocpi.modules.cdrs.v_2_2_1.enums import AuthMethod
from py_ocpi.modules.tokens.v_2_2_1.enums import WhitelistType, TokenType
from py_ocpi.modules.tokens.v_2_2_1.schemas import Token
from py_ocpi.modules.versions.enums import VersionNumber

TOKENS = [
    {
        'country_code': 'us',
        'party_id': 'AAA',
        'uid': str(uuid4()),
        'type': TokenType.rfid,
        'contract_id': str(uuid4()),
        'issuer': 'issuer',
        'auth_method': AuthMethod.auth_request,
        'valid': True,
        'whitelist': WhitelistType.always,
        'last_updated': '2022-01-02 00:00:00+00:00'
    }
]

TOKEN_UPDATE = {
    'country_code': 'pl',
    'party_id': 'BBB',
    'last_updated': '2022-01-02 00:00:00+00:00'
}


class Crud:

    @classmethod
    async def get(cls, module: enums.ModuleID, filters: dict, *args, **kwargs) -> Token:
        return TOKENS[0]

    @classmethod
    async def create(cls, module: enums.ModuleID, data: Token, *args, **kwargs) -> dict:
        return data

    @classmethod
    async def update(cls, module: enums.ModuleID, data: Token, id: str, *args, **kwargs):
        data = dict(data)
        TOKENS[0]['country_code'] = data['country_code']
        TOKENS[0]['party_id'] = data['party_id']
        return TOKENS[0]


class Adapter:
    @classmethod
    def token_adapter(cls, data) -> Token:
        return Token(**dict(data))


def test_get_token():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.get(f'/ocpi/cpo/2.2.1/tokens/{TOKENS[0]["country_code"]}/{TOKENS[0]["party_id"]}/'
                          f'{TOKENS[0]["uid"]}')

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['uid'] == TOKENS[0]["uid"]


def test_add_token():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.put(f'/ocpi/cpo/2.2.1/tokens/{TOKENS[0]["country_code"]}/{TOKENS[0]["party_id"]}/'
                          f'{TOKENS[0]["uid"]}', json=TOKENS[0])

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['uid'] == TOKENS[0]["uid"]


def test_update_token():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.patch(f'/ocpi/cpo/2.2.1/tokens/{TOKENS[0]["country_code"]}/{TOKENS[0]["party_id"]}/'
                            f'{TOKENS[0]["uid"]}', json=TOKEN_UPDATE)

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['country_code'] == TOKEN_UPDATE['country_code']
