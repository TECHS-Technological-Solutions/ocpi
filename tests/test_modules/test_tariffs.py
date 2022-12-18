from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi.main import get_application
from py_ocpi.core import enums
from py_ocpi.core.config import settings
from py_ocpi.modules.tariffs.v_2_2_1.schemas import Tariff
from py_ocpi.modules.versions.enums import VersionNumber

TARIFFS = [{
    'country_code': 'MY',
    'party_id': 'JOM',
    'id': str(uuid4()),
    'currency': 'MYR',
    'type': 'REGULAR',
    'elements': [
        {
            'price_components': [
                {
                    'type': 'ENERGY',
                    'price': 1.50,
                    'step_size': 2
                },
            ]
        },
    ],
    'last_updated': '2022-01-02 00:00:00+00:00'
},
]


class Crud:
    @classmethod
    async def get(cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs):
        return TARIFFS[0]

    @classmethod
    async def update(cls, module: enums.ModuleID, role: enums.RoleEnum, data: dict, id, *args, **kwargs):
        return data

    @classmethod
    async def create(cls, module: enums.ModuleID, role: enums.RoleEnum, data: dict, *args, **kwargs):
        return data

    @classmethod
    async def delete(cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs):
        ...

    @classmethod
    async def list(cls, module: enums.ModuleID, role: enums.RoleEnum, filters: dict, *args, **kwargs) -> list:
        return TARIFFS, 1, True


class Adapter:
    @classmethod
    def tariff_adapter(cls, data, version: VersionNumber = VersionNumber.latest) -> Tariff:
        return Tariff(**data)


def test_cpo_get_tariffs_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.get('/ocpi/cpo/2.2.1/tariffs')

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['id'] == TARIFFS[0]["id"]


def test_emsp_get_tariff_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.get(f'/ocpi/emsp/2.2.1/tariffs/{settings.COUNTRY_CODE}/{settings.PARTY_ID}'
                          f'/{TARIFFS[0]["id"]}')

    assert response.status_code == 200
    assert response.json()['data'][0]['id'] == TARIFFS[0]["id"]


def test_emsp_add_tariff_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.put(f'/ocpi/emsp/2.2.1/tariffs/{settings.COUNTRY_CODE}/{settings.PARTY_ID}'
                          f'/{TARIFFS[0]["id"]}', json=TARIFFS[0])
    print(response.json())
    assert response.status_code == 200
    assert response.json()['data'][0]['id'] == TARIFFS[0]["id"]


def test_emsp_delete_tariff_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.delete(f'/ocpi/emsp/2.2.1/tariffs/{settings.COUNTRY_CODE}/{settings.PARTY_ID}'
                             f'/{TARIFFS[0]["id"]}')

    assert response.status_code == 200
