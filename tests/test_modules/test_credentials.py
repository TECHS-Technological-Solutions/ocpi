import functools
from uuid import uuid4
from unittest.mock import patch
from typing import Any

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from py_ocpi import get_application
from py_ocpi.core import enums
from py_ocpi.core.data_types import URL
from py_ocpi.core.config import settings
from py_ocpi.core.dependencies import get_versions
from py_ocpi.core.utils import encode_string_base64
from py_ocpi.modules.credentials.v_2_2_1.schemas import Credentials
from py_ocpi.modules.tokens.v_2_2_1.enums import AllowedType
from py_ocpi.modules.tokens.v_2_2_1.schemas import AuthorizationInfo, Token
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.versions.schemas import Version

CREDENTIALS_TOKEN_GET = {
    'url': 'url',
    'roles': [{
        'role': enums.RoleEnum.emsp,
        'business_details': {
            'name': 'name',
        },
        'party_id': 'JOM',
        'country_code': 'MY'
    }]
}

CREDENTIALS_TOKEN = {
    'token': str(uuid4()),
    'url': '/ocpi/versions',
    'roles': [{
        'role': enums.RoleEnum.emsp,
        'business_details': {
            'name': 'name',
        },
        'party_id': 'JOM',
        'country_code': 'MY'
    }]
}


def partial_class(cls, *args, **kwds):

    class NewCls(cls):
        __init__ = functools.partialmethod(cls.__init__, *args, **kwds)

    return NewCls


class Crud:
    @classmethod
    async def get(cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs):
        if id == CREDENTIALS_TOKEN['token']:
            return None
        return dict(CREDENTIALS_TOKEN_GET, **{'token': id})

    @classmethod
    async def create(cls, module: enums.ModuleID, data, operation, *args, **kwargs):
        if operation == 'credentials':
            return None
        return CREDENTIALS_TOKEN

    @classmethod
    async def update(cls, module: enums.ModuleID, data, operation, *args, **kwargs):
        if operation == 'credentials':
            return None
        return CREDENTIALS_TOKEN

    @classmethod
    async def do(cls, module: enums.ModuleID, role: enums.RoleEnum, action: enums.Action, *args,
                 data: dict = None, **kwargs):
        return None


class Adapter:
    @classmethod
    def credentials_adapter(cls, data, version: VersionNumber = VersionNumber.latest) -> Credentials:
        return Credentials(**data)


def test_cpo_get_credentials_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)
    token = str(uuid4())
    header = {
        "Authorization": f'Token {encode_string_base64(token)}'
    }

    client = TestClient(app)
    response = client.get('/ocpi/cpo/2.2.1/credentials', headers=header)

    assert response.status_code == 200
    assert response.json()['data']['token'] == token


@pytest.mark.asyncio
@patch('py_ocpi.modules.credentials.v_2_2_1.api.cpo.httpx.AsyncClient')
async def test_cpo_post_credentials_v_2_2_1(async_client):
    class MockCrud(Crud):
        @classmethod
        async def do(cls, module: enums.ModuleID, role: enums.RoleEnum, action: enums.Action, auth_token, *args, data: dict = None, **kwargs) -> Any:
            return {}

    app_1 = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], MockCrud, Adapter)

    def override_get_versions():
        return [
            Version(
                version=VersionNumber.v_2_2_1,
                url=URL(f'/{settings.OCPI_PREFIX}/{VersionNumber.v_2_2_1.value}/details')
            ).dict()
        ]

    app_1.dependency_overrides[get_versions] = override_get_versions

    async_client.return_value = AsyncClient(app=app_1, base_url="http://test")


    app_2 = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], MockCrud, Adapter)

    async with AsyncClient(app=app_2, base_url="http://test") as client:
        response = await client.post('/ocpi/cpo/2.2.1/credentials/', json=CREDENTIALS_TOKEN)

    assert response.status_code == 200
    assert response.json()['data']['token'] == CREDENTIALS_TOKEN['token']

@pytest.mark.asyncio
@patch('py_ocpi.modules.credentials.v_2_2_1.api.cpo.httpx.AsyncClient')
async def test_cpo_put_credentials_v_2_2_1(async_client):
    class MockCrud(Crud):
        @classmethod
        async def do(cls, module: enums.ModuleID, role: enums.RoleEnum, action: enums.Action, auth_token, *args, data: dict = None, **kwargs) -> Any:
            return {'dummy':'is_registered'}

    app_1 = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], MockCrud, Adapter)

    def override_get_versions():
        return [
            Version(
                version=VersionNumber.v_2_2_1,
                url=URL(f'/{settings.OCPI_PREFIX}/{VersionNumber.v_2_2_1.value}/details')
            ).dict()
        ]

    app_1.dependency_overrides[get_versions] = override_get_versions

    async_client.return_value = AsyncClient(app=app_1, base_url="http://test")

    app_2 = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], MockCrud, Adapter)

    async with AsyncClient(app=app_2, base_url="http://test") as client:
        response = await client.put('/ocpi/cpo/2.2.1/credentials/', json=CREDENTIALS_TOKEN)

    assert response.status_code == 200
    assert response.json()['data']['token'] == CREDENTIALS_TOKEN['token']