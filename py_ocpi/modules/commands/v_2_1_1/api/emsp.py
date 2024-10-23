from fastapi import APIRouter, Depends, Request

from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.config import logger
from py_ocpi.core import status
from py_ocpi.core.utils import get_auth_token
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.commands.v_2_1_1.schemas import CommandResponse

router = APIRouter(
    prefix="/commands",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_1_1))],
)


@router.post("/{uid}", response_model=OCPIResponse)
async def receive_command_result(
    request: Request,
    uid: str,
    command_response: CommandResponse,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Receive Command Result.

    Processes and handles incoming command results.

    **Path parameters:**
        - uid (str): The unique identifier associated with the command.

    **Request body:**
        command_response (CommandResponse): The response data associated
            with the command.

    **Returns:**
        The OCPIResponse indicating the success or failure of processing
            the command result.
    """
    logger.info("Received command result with uid - `%s`." % uid)
    logger.debug("Command response data - %s" % command_response.dict())
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    await crud.update(
        ModuleID.commands,
        RoleEnum.emsp,
        command_response.dict(),
        uid,
        auth_token=auth_token,
        version=VersionNumber.v_2_1_1,
    )

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
