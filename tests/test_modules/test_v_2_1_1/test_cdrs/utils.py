from uuid import uuid4

from py_ocpi.core import enums
from py_ocpi.modules.cdrs.v_2_1_1.enums import AuthMethod, CdrDimensionType

from tests.test_modules.utils import (
    AUTH_TOKEN,
    RANDOM_AUTH_TOKEN,
    ClientAuthenticator,
)
from tests.test_modules.test_v_2_1_1.test_locations.utils import LOCATIONS


CPO_BASE_URL = "/ocpi/cpo/2.1.1/cdrs/"
EMSP_BASE_URL = "/ocpi/emsp/2.1.1/cdrs/"
AUTH_HEADERS = {"Authorization": f"Token {AUTH_TOKEN}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {RANDOM_AUTH_TOKEN}"}

CDRS = [
    {
        "id": str(uuid4()),
        "start_date_time": "2022-01-02 00:00:00+00:00",
        "end_date_time": "2022-01-02 00:00:00+00:00",
        "auth_id": "DE8ACC12E46L89",
        "auth_method": AuthMethod.auth_request,
        "location": LOCATIONS[0],
        "currency": "EUR",
        "tariffs": [
            {
                "id": "12",
                "currency": "EUR",
                "elements": [
                    {
                        "price_components": [
                            {"type": "TIME", "price": "2.00", "step_size": 300}
                        ]
                    }
                ],
                "last_updated": "2022-01-02 00:00:00+00:00",
            }
        ],
        "charging_periods": [
            {
                "start_date_time": "2022-01-02 00:00:00+00:00",
                "dimensions": [
                    {"type": CdrDimensionType.time, "volume": 1.973}
                ],
            }
        ],
        "total_cost": 4.00,
        "total_energy": 15.342,
        "total_time": 1.973,
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]


class Crud:
    @classmethod
    async def list(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> list:
        return CDRS, 1, True

    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return CDRS[0]

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
