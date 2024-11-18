import functools
from uuid import uuid4

from py_ocpi.core import enums

from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN,
    ENCODED_AUTH_TOKEN_A,
    AUTH_TOKEN_A_V_2_2_1,
    ENCODED_RANDOM_AUTH_TOKEN,
    ClientAuthenticator,
)

AUTH_HEADERS_A = {"Authorization": f"Token {ENCODED_AUTH_TOKEN_A}"}
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN}"}

CREDENTIALS_TOKEN_GET = {
    "url": "url",
    "roles": [
        {
            "role": enums.RoleEnum.emsp,
            "business_details": {
                "name": "name",
            },
            "party_id": "JOM",
            "country_code": "MY",
        }
    ],
}

CREDENTIALS_TOKEN_CREATE = {
    "token": AUTH_TOKEN_A_V_2_2_1,
    "url": "/ocpi/versions",
    "roles": [
        {
            "role": enums.RoleEnum.emsp,
            "business_details": {
                "name": "name",
            },
            "party_id": "JOM",
            "country_code": "MY",
        }
    ],
}


def partial_class(cls, *args, **kwds):
    class NewCls(cls):
        __init__ = functools.partialmethod(cls.__init__, *args, **kwds)

    return NewCls


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return CREDENTIALS_TOKEN_CREATE

    @classmethod
    async def create(
        cls, module: enums.ModuleID, data, operation, *args, **kwargs
    ):
        if operation == "credentials":
            return None
        return CREDENTIALS_TOKEN_CREATE

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
        return None
