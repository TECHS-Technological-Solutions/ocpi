from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi.main import get_application
from py_ocpi.core import enums
from py_ocpi.core.config import settings
from py_ocpi.modules.cdrs.v_2_2_1.schemas import TokenType
from py_ocpi.modules.cdrs.v_2_2_1.enums import AuthMethod, CdrDimensionType
from py_ocpi.modules.sessions.v_2_2_1.schemas import Session, ChargingPreferences
from py_ocpi.modules.sessions.v_2_2_1.enums import SessionStatus, ProfileType
from py_ocpi.modules.versions.enums import VersionNumber

SESSIONS = [
    {
        'country_code': 'us',
        'party_id': 'AAA',
        'id': str(uuid4()),
        'start_date_time': '2022-01-02 00:00:00+00:00',
        'end_date_time': '2022-01-02 00:05:00+00:00',
        'kwh': 100,
        'cdr_token': {
            'country_code': 'us',
            'party_id': 'AAA',
            'uid': str(uuid4()),
            'type': TokenType.rfid,
            'contract_id': str(uuid4())
        },
        'auth_method': AuthMethod.auth_request,
        'location_id': str(uuid4()),
        'evse_uid': str(uuid4()),
        'connector_id': str(uuid4()),
        'currency': 'MYR',
        'charging_periods': [
            {
                'start_date_time': '2022-01-02 00:00:00+00:00',
                'dimensions': [
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
        'status': SessionStatus.active,
        'last_updated': '2022-01-02 00:00:00+00:00'
    }
]

CHARGING_PREFERENCES = {
    'profile_type': ProfileType.fast,
    'departure_time': '2022-01-02 00:00:00+00:00',
    'energy_need': 100
}


class Crud:

    @classmethod
    async def get(cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs):
        return SESSIONS[0]

    @classmethod
    async def update(cls, module: enums.ModuleID, role: enums.RoleEnum, data: dict, id, *args, **kwargs):
        return data

    @classmethod
    async def create(cls, module: enums.ModuleID, role: enums.RoleEnum, data: dict, *args, **kwargs):
        return data

    @classmethod
    async def list(cls, module: enums.ModuleID, role: enums.RoleEnum, filters: dict, *args, **kwargs) -> list:
        return SESSIONS, 1, True


class Adapter:
    @classmethod
    def session_adapter(cls, data, version: VersionNumber = VersionNumber.latest) -> Session:
        return Session(**data)

    @classmethod
    def charging_preference_adapter(cls, data, version: VersionNumber = VersionNumber.latest) -> Session:
        return ChargingPreferences(**data)


def test_cpo_get_sessions_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.get('/ocpi/cpo/2.2.1/sessions')

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['id'] == SESSIONS[0]["id"]


def test_cpo_set_charging_preference_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.put(f'/ocpi/cpo/2.2.1/sessions/{SESSIONS[0]["id"]}/charging_preferences',
                          json=CHARGING_PREFERENCES)

    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]['energy_need'] == CHARGING_PREFERENCES["energy_need"]


def test_emsp_get_session_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.get(f'/ocpi/emsp/2.2.1/sessions/{settings.COUNTRY_CODE}/{settings.PARTY_ID}'
                          f'/{SESSIONS[0]["id"]}')

    assert response.status_code == 200
    assert response.json()['data'][0]['id'] == SESSIONS[0]["id"]


def test_emsp_add_session_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    client = TestClient(app)
    response = client.put(f'/ocpi/emsp/2.2.1/sessions/{settings.COUNTRY_CODE}/{settings.PARTY_ID}'
                          f'/{SESSIONS[0]["id"]}', json=SESSIONS[0])

    assert response.status_code == 200
    assert response.json()['data'][0]['id'] == SESSIONS[0]["id"]


def test_emsp_patch_session_v_2_2_1():
    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.emsp], Crud, Adapter)

    patch_data = {'id': str(uuid4())}
    client = TestClient(app)
    response = client.patch(f'/ocpi/emsp/2.2.1/sessions/{settings.COUNTRY_CODE}/{settings.PARTY_ID}'
                            f'/{SESSIONS[0]["id"]}', json=patch_data)

    assert response.status_code == 200
    assert response.json()['data'][0]['id'] == patch_data["id"]
