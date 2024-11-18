from py_ocpi.core import enums
from py_ocpi.modules.hubclientinfo.v_2_2_1.enums import ConnectionStatus
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN,
    ENCODED_RANDOM_AUTH_TOKEN,
)

CPO_BASE_URL = "/ocpi/cpo/2.2.1/clientinfo/"
EMSP_BASE_URL = "/ocpi/emsp/2.2.1/clientinfo/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN}"}


CLIENT_INFO = [
    {
        "party_id": "aaa",
        "country_code": "us",
        "role": enums.RoleEnum.cpo,
        "status": ConnectionStatus.connected,
        "last_updated": "2022-01-01 00:00:00+00:00",
    }
]


class Crud:
    @classmethod
    async def get(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        id,
        *args,
        **kwargs,
    ):
        return CLIENT_INFO[0]

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
