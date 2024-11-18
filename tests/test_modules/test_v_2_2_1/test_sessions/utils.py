from uuid import uuid4

from py_ocpi.core import enums
from py_ocpi.modules.cdrs.v_2_2_1.schemas import TokenType
from py_ocpi.modules.cdrs.v_2_2_1.enums import AuthMethod, CdrDimensionType
from py_ocpi.modules.sessions.v_2_2_1.enums import SessionStatus, ProfileType

from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN,
    ENCODED_RANDOM_AUTH_TOKEN,
    ClientAuthenticator,
)

CPO_BASE_URL = "/ocpi/cpo/2.2.1/sessions/"
EMSP_BASE_URL = "/ocpi/emsp/2.2.1/sessions/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN}"}

SESSIONS = [
    {
        "country_code": "us",
        "party_id": "AAA",
        "id": str(uuid4()),
        "start_date_time": "2022-01-02 00:00:00+00:00",
        "end_date_time": "2022-01-02 00:05:00+00:00",
        "kwh": 100,
        "cdr_token": {
            "country_code": "us",
            "party_id": "AAA",
            "uid": str(uuid4()),
            "type": TokenType.rfid,
            "contract_id": str(uuid4()),
        },
        "auth_method": AuthMethod.auth_request,
        "location_id": str(uuid4()),
        "evse_uid": str(uuid4()),
        "connector_id": str(uuid4()),
        "currency": "MYR",
        "charging_periods": [
            {
                "start_date_time": "2022-01-02 00:00:00+00:00",
                "dimensions": [{"type": CdrDimensionType.power, "volume": 10}],
            }
        ],
        "total_cost": {"excl_vat": 10.0000, "incl_vat": 10.2500},
        "status": SessionStatus.active,
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]

CHARGING_PREFERENCES = {
    "profile_type": ProfileType.fast,
    "departure_time": "2022-01-02 00:00:00+00:00",
    "energy_need": 100,
}


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return SESSIONS[0]

    @classmethod
    async def update(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        id,
        *args,
        **kwargs,
    ):
        return data

    @classmethod
    async def create(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        *args,
        **kwargs,
    ):
        return data

    @classmethod
    async def list(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> list:
        return SESSIONS, 1, True
