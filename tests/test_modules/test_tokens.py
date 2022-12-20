from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi.main import get_application
from py_ocpi.core import enums
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.modules.cdrs.v_2_2_1.enums import AuthMethod
from py_ocpi.modules.tokens.v_2_2_1.enums import WhitelistType, TokenType, AllowedType
from py_ocpi.modules.tokens.v_2_2_1.schemas import AuthorizationInfo, Token
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
    async def get(cls, module: enums.ModuleID, role: enums.RoleEnum, filters: dict, *args, **kwargs) -> Token:
        return TOKENS[0]

    @classmethod
    async def create(cls, module: enums.ModuleID, role: enums.RoleEnum, data: Token, *args, **kwargs) -> dict:
        return data

    @classmethod
    async def do(cls, module: enums.ModuleID, role: enums.RoleEnum, action: enums.Action, *args,
                 data: dict = None, **kwargs):
        return AuthorizationInfo(
            allowed=AllowedType.allowed,
            token=Token(**TOKENS[0])
        ).dict()

    @classmethod
    async def list(cls, module: enums.ModuleID, role: enums.RoleEnum, filters: dict, *args, **kwargs) -> list:
        return TOKENS, 1, True

    @classmethod
    async def update(cls, module: enums.ModuleID, role: enums.RoleEnum, data: Token, id: str, *args, **kwargs):
        data = dict(data)
        TOKENS[0]['country_code'] = data['country_code']
        TOKENS[0]['party_id'] = data['party_id']
        return TOKENS[0]


class Adapter:
    @classmethod
    def token_adapter(cls, data, version: VersionNumber = VersionNumber.latest) -> Token:
        return Token(**dict(data))

    @classmethod
    def authorization_adapter(cls, data: dict, version: VersionNumber = VersionNumber.latest):
        return AuthorizationInfo(**data)


def test_cpo_get_token_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.get(f'/ocpi/cpo/2.2.1/tokens/{TOKENS[0]["country_code"]}/{TOKENS[0]["party_id"]}/'
                          f'{TOKENS[0]["uid"]}')

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['uid'] == TOKENS[0]["uid"]


def test_cpo_add_token_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.put(f'/ocpi/cpo/2.2.1/tokens/{TOKENS[0]["country_code"]}/{TOKENS[0]["party_id"]}/'
                          f'{TOKENS[0]["uid"]}', json=TOKENS[0])

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['uid'] == TOKENS[0]["uid"]


def test_cpo_update_token_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.patch(f'/ocpi/cpo/2.2.1/tokens/{TOKENS[0]["country_code"]}/{TOKENS[0]["party_id"]}/'
                            f'{TOKENS[0]["uid"]}', json=TOKEN_UPDATE)

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['country_code'] == TOKEN_UPDATE['country_code']


def test_emsp_get_tokens_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.get('/ocpi/emsp/2.2.1/tokens')

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['uid'] == TOKENS[0]["uid"]


def test_emsp_authorize_token_success_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.post(f'/ocpi/emsp/2.2.1/tokens/{TOKENS[0]["uid"]}/authorize')

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['allowed'] == AllowedType.allowed


def test_emsp_authorize_token_unknown_v_2_2_1():

    @classmethod
    async def get(cls, module: enums.ModuleID, role: enums.RoleEnum, filters: dict, *args, **kwargs) -> Token:
        raise NotFoundOCPIError()
    _get = Crud.get
    Crud.get = get

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.post(f'/ocpi/emsp/2.2.1/tokens/{TOKENS[0]["uid"]}/authorize')

    assert response.status_code == 404
    assert response.json()['status_code'] == 2004

    # revert Crud changes
    Crud.get = _get


def test_emsp_authorize_token_missing_info_v_2_2_1():

    @classmethod
    async def do(cls, module: enums.ModuleID, role: enums.RoleEnum, action: enums.Action, *args,
                 data: dict = None, **kwargs):
        return False
    _do = Crud.do
    Crud.do = do

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.post(f'/ocpi/emsp/2.2.1/tokens/{TOKENS[0]["uid"]}/authorize')

    assert response.status_code == 200
    assert response.json()['status_code'] == 2002

    # revert Crud changes
    Crud.do = _do
