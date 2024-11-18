import functools
from uuid import uuid4

from py_ocpi.core import enums

from tests.test_modules.utils import (
    AUTH_TOKEN,
    AUTH_TOKEN_A,
    RANDOM_AUTH_TOKEN,
    ClientAuthenticator,
)

AUTH_HEADERS = {"Authorization": f"Token {AUTH_TOKEN}"}
AUTH_HEADERS_A = {"Authorization": f"Token {AUTH_TOKEN_A}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {RANDOM_AUTH_TOKEN}"}


CREDENTIALS_TOKEN_GET = {
    "url": "url",
    "business_details": {
        "name": "name",
    },
    "party_id": "JOM",
    "country_code": "MY",
}

CREDENTIALS_TOKEN_CREATE = {
    "token": AUTH_TOKEN_A,
    "url": "/ocpi/versions",
    "business_details": {
        "name": "name",
    },
    "party_id": "JOM",
    "country_code": "MY",
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
