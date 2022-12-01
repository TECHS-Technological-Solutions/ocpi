from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi.core import enums
from py_ocpi.locations.v_2_2_1.schemas import ConnectorType, ConnectorFormat, PowerType
from py_ocpi.cdrs.v_2_2_1.schemas import TokenType, Cdr
from py_ocpi.cdrs.v_2_2_1.enums import AuthMethod, CdrDimensionType
from py_ocpi.main import get_application
from py_ocpi.versions.enums import VersionNumber

CDRS = [
    {
        'country_code': 'us',
        'party_id': 'AAA',
        'id': str(uuid4()),
        'start_date_time': '2022-01-02 00:00:00+00:00',
        'end_date_time': '2022-01-02 00:05:00+00:00',
        'cdr_token': {
            'country_code': 'us',
            'party_id': 'AAA',
            'uid': str(uuid4()),
            'type': TokenType.rfid,
            'contract_id': str(uuid4())
        },
        'auth_method': AuthMethod.auth_request,
        'cdr_location': {
            'id': str(uuid4()),
            'name': 'name',
            'address': 'address',
            'city': 'city',
            'postal_code': '111111',
            'state': 'state',
            'country': 'USA',
            'coordinates': {
                'latitude': 'latitude',
                'longitude': 'longitude',
            },
            'evse_id': str(uuid4()),
            'connector_id': str(uuid4()),
            'connector_standard': ConnectorType.tesla_r,
            'connector_format': ConnectorFormat.cable,
            'connector_power_type': PowerType.dc
        },
        'currency': 'MYR',
        'charging_periods': [
            {
                'start_date_time': '2022-01-02 00:00:00+00:00',
                'diemnsions': [
                    {
                        'type': CdrDimensionType.power,
                        'volume': 10
                    }
                ]
            }
        ],
        'total_cost': {
            'excl_vat': 10.0000,
            'incl_vat': 10.2500
        },
        'total_energy': 50,
        'total_time': 500,
        'last_updated': '2022-01-02 00:00:00+00:00'
    }
]


class Crud:

    @classmethod
    async def list(cls, module: enums.ModuleID, filters: dict, *args, **kwargs) -> list:
        return CDRS, 1, True


class Adapter:
    @classmethod
    def cdr_adapter(cls, data) -> Cdr:
        return Cdr(**data)


def test_get_cdrs():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.get('/ocpi/cpo/2.2.1/cdrs')

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['id'] == CDRS[0]["id"]
