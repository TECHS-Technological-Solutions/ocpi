from uuid import uuid4

from py_ocpi.core import enums

from py_ocpi.modules.tokens.v_2_1_1.enums import (
    WhitelistType,
    TokenType,
    Allowed,
)
from py_ocpi.modules.tokens.v_2_1_1.schemas import AuthorizationInfo, Token

from tests.test_modules.utils import (
    AUTH_TOKEN,
    RANDOM_AUTH_TOKEN,
    ClientAuthenticator,
)

CPO_BASE_URL = "/ocpi/cpo/2.1.1/tokens/"
EMSP_BASE_URL = "/ocpi/emsp/2.1.1/tokens/"
AUTH_HEADERS = {"Authorization": f"Token {AUTH_TOKEN}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {RANDOM_AUTH_TOKEN}"}

TOKENS = [
    {
        "uid": str(uuid4()),
        "type": TokenType.rfid,
        "auth_id": str(uuid4()),
        "issuer": "issuer",
        "valid": True,
        "whitelist": WhitelistType.always,
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]

TOKEN_UPDATE = {
    "valid": False,
}


class Crud:
    @classmethod
    async def get(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> Token:
        return TOKENS[0]

    @classmethod
    async def create(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: Token,
        *args,
        **kwargs,
    ) -> dict:
        return data

    @classmethod
    async def do(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        action: enums.Action,
        *args,
        data: dict = None,
        **kwargs,
    ):
        return AuthorizationInfo(
            allowed=Allowed.allowed, token=Token(**TOKENS[0])
        ).dict()

    @classmethod
    async def list(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> list:
        return TOKENS, 1, True

    @classmethod
    async def update(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: Token,
        id: str,
        *args,
        **kwargs,
    ):
        data = dict(data)
        TOKENS[0]["valid"] = data["valid"]
        return TOKENS[0]
