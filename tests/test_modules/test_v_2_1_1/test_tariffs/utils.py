from uuid import uuid4

from py_ocpi.core import enums

from tests.test_modules.utils import (
    AUTH_TOKEN,
    RANDOM_AUTH_TOKEN,
    ClientAuthenticator,
)

CPO_BASE_URL = "/ocpi/cpo/2.1.1/tariffs/"
EMSP_BASE_URL = "/ocpi/emsp/2.1.1/tariffs/"
AUTH_HEADERS = {"Authorization": f"Token {AUTH_TOKEN}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {RANDOM_AUTH_TOKEN}"}

TARIFFS = [
    {
        "id": str(uuid4()),
        "currency": "MYR",
        "elements": [
            {
                "price_components": [
                    {
                        "type": "ENERGY",
                        "price": 1.50,
                        "step_size": 2,
                    },
                ]
            },
        ],
        "last_updated": "2022-01-02 00:00:00+00:00",
    },
]


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return TARIFFS[0]

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
    async def delete(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        ...

    @classmethod
    async def list(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> list:
        return TARIFFS, 1, True
