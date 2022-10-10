from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi.core import enums
from py_ocpi.tariffs.v_2_2_1.schemas import Tariff
from py_ocpi.main import get_application
from py_ocpi.versions.enums import VersionNumber

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
    async def list(cls, module: enums.ModuleID, filters: dict, *args, **kwargs) -> list:
        return TARIFFS, 1, True


class Adapter:
    @classmethod
    def tariff_adapter(cls, data) -> Tariff:
        return Tariff(**data)


def test_get_tariffs():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.get('/ocpi/cpo/2.2.1/tariffs')

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['id'] == TARIFFS[0]["id"]
