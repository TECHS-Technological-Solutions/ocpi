from uuid import uuid4

from fastapi.testclient import TestClient
from unittest.mock import patch

from py_ocpi.core import enums
from py_ocpi.credentials.v_2_2_1.schemas import Credentials
from py_ocpi.main import get_application
from py_ocpi.versions.enums import VersionNumber
from tests.test_modules.mocks.async_client import MockAsyncClientGeneratorVersionsAndEndpoints

CREDENTIALS_GET = {
    'url': 'url',
    'roles': [{
        'role': enums.RoleEnum.cpo,
        'business_details': {
            'name': 'name',
        },
        'party_id': 'JOM',
        'country_code': 'MY'
    }]
}

CREDENTIALS_CREATE = {
    'token': str(uuid4()),
    'url': 'url',
    'roles': [{
        'role': enums.RoleEnum.cpo,
        'business_details': {
            'name': 'name',
        },
        'party_id': 'JOM',
        'country_code': 'MY'
    }]
}


class Crud:
    @classmethod
    async def get(cls, module: enums.ModuleID, id, *args, **kwargs):
        if id == CREDENTIALS_CREATE['token']:
            return None
        return dict(CREDENTIALS_GET, **{'token': id})

    @classmethod
    async def create(cls, module: enums.ModuleID, data, *args, **kwargs):
        if 'cred_token_b' in data:
            return None
        return CREDENTIALS_CREATE


class Adapter:
    @classmethod
    def credentials_adapter(cls, data) -> Credentials:
        return Credentials(**data)


def test_get_credentials():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)
    token = str(uuid4())
    header = {
        "Authorization": f'Token {token}'
    }

    client = TestClient(app)
    response = client.get(f'/ocpi/cpo/2.2.1/credentials', headers=header)

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['token'] == token


@patch('py_ocpi.credentials.v_2_2_1.api.cpo.httpx.AsyncClient', side_effect=MockAsyncClientGeneratorVersionsAndEndpoints)
def test_post_credentials(async_mock):
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.post(f'/ocpi/cpo/2.2.1/credentials/create', json=CREDENTIALS_CREATE)

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['token'] == CREDENTIALS_CREATE['token']
