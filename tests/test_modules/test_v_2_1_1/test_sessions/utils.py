from uuid import uuid4

from py_ocpi.core import enums
from py_ocpi.modules.cdrs.v_2_1_1.enums import AuthMethod, CdrDimensionType
from py_ocpi.modules.sessions.v_2_1_1.enums import SessionStatus

from tests.test_modules.utils import (
    AUTH_TOKEN,
    RANDOM_AUTH_TOKEN,
    ClientAuthenticator,
)
from tests.test_modules.test_v_2_1_1.test_locations.utils import LOCATIONS

CPO_BASE_URL = "/ocpi/cpo/2.1.1/sessions/"
EMSP_BASE_URL = "/ocpi/emsp/2.1.1/sessions/"
AUTH_HEADERS = {"Authorization": f"Token {AUTH_TOKEN}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {RANDOM_AUTH_TOKEN}"}

SESSIONS = [
    {
        "id": str(uuid4()),
        "start_datetime": "2022-01-02 00:00:00+00:00",
        "end_datetime": "2022-01-02 00:05:00+00:00",
        "kwh": 100,
        "auth_id": "100",
        "auth_method": AuthMethod.auth_request,
        "location": LOCATIONS[0],
        "currency": "MYR",
        "charging_periods": [
            {
                "start_date_time": "2022-01-02 00:00:00+00:00",
                "dimensions": [
                    {
                        "type": CdrDimensionType.time,
                        "volume": 10,
                    }
                ],
            }
        ],
        "status": SessionStatus.active,
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]


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
