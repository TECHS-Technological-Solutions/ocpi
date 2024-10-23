from py_ocpi.core import enums
from py_ocpi.modules.commands.v_2_2_1.enums import (
    CommandResponseType,
    CommandResultType,
)

from tests.test_modules.utils import (
    AUTH_TOKEN,
    RANDOM_AUTH_TOKEN,
    ClientAuthenticator,
)

CPO_BASE_URL = "/ocpi/cpo/2.1.1/commands/"
EMSP_BASE_URL = "/ocpi/emsp/2.1.1/commands/"
AUTH_HEADERS = {"Authorization": f"Token {AUTH_TOKEN}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {RANDOM_AUTH_TOKEN}"}

COMMAND_RESPONSE = {"result": CommandResponseType.accepted}


class Crud:
    @classmethod
    async def do(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        action: enums.Action,
        *args,
        data: dict = None,
        **kwargs,
    ) -> dict:
        if action == enums.Action.get_client_token:
            return "foo"

        return COMMAND_RESPONSE

    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ) -> dict:
        return COMMAND_RESPONSE

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
        ...
