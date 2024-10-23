from asyncio import sleep

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Request,
    status as fastapistatus,
)
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import httpx

from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core.enums import ModuleID, RoleEnum, Action
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.config import logger
from py_ocpi.core import status
from py_ocpi.core.config import settings
from py_ocpi.core.utils import get_auth_token
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.commands.v_2_1_1.enums import CommandType
from py_ocpi.modules.commands.v_2_1_1.schemas import (
    ReserveNow,
    StartSession,
    StopSession,
    UnlockConnector,
    CommandResponse,
    CommandResponseType,
)

router = APIRouter(
    prefix="/commands",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_1_1))],
)


async def apply_pydantic_schema(command: str, data: dict):
    if command == CommandType.reserve_now:
        data = ReserveNow(**data)  # type: ignore
    elif command == CommandType.start_session:
        data = StartSession(**data)  # type: ignore
    elif command == CommandType.stop_session:
        data = StopSession(**data)  # type: ignore
    elif command == CommandType.unlock_connector:
        data = UnlockConnector(**data)  # type: ignore
    else:
        raise NotImplementedError
    return data


async def send_command_result(
    command_data: StartSession | StopSession | ReserveNow | UnlockConnector,
    command: CommandType,
    auth_token: str,
    crud: Crud,
    adapter: Adapter,
):
    client_auth_token = await crud.do(
        ModuleID.commands,
        RoleEnum.cpo,
        Action.get_client_token,
        auth_token=auth_token,
        version=VersionNumber.v_2_1_1,
    )

    command_result = None
    for _ in range(30 * settings.COMMAND_AWAIT_TIME):
        # since command has no id, 0 is used for id parameter of crud.get
        command_result = await crud.get(
            ModuleID.commands,
            RoleEnum.cpo,
            0,
            command_data=command_data,
            auth_token=auth_token,
            version=VersionNumber.v_2_1_1,
            command=command,
        )
        if command_result:
            logger.info(
                "Command result from Charge Point - %s" % command_result
            )
            break
        await sleep(2)

    if not command_result:
        logger.info("Command result from Charge Point didn't arrive in time.")
        command_response = CommandResponse(result=CommandResponseType.timeout)
    else:
        command_response = adapter.command_response_adapter(
            command_result, VersionNumber.v_2_1_1
        )

    async with httpx.AsyncClient() as client:
        authorization_token = f"Token {client_auth_token}"
        logger.info(
            "Send request with command result: %s" % command_data.response_url
        )
        res = await client.post(
            command_data.response_url,
            json=command_response.dict(),
            headers={"authorization": authorization_token},
        )
        logger.info(
            "POST command data after receiving result from Charge Point"
            " status_code: %s" % res.status_code
        )


@router.post("/{command}", response_model=OCPIResponse)
async def receive_command(
    request: Request,
    command: CommandType,
    data: dict,
    background_tasks: BackgroundTasks,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Receive Command.

    Processes and handles incoming commands.

    **Path parameters:**
        - command (CommandType): The type of the command.

    **Request body:**
        data (dict): The data associated with the command.

    **Returns:**
        The OCPIResponse indicating the success or failure of the command.

    **Raises:**
        - HTTPException: If there is a validation error or
            if the command action returns without a result.
        - NotFoundOCPIError: If the associated location is not found.
    """
    logger.info("Received command - `%s`." % command)
    logger.debug("Command data - %s" % data)
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    try:
        command_data = await apply_pydantic_schema(command, data)
    except ValidationError as exc:
        logger.debug("ValidationError on applying pydantic schema to command")
        return JSONResponse(
            status_code=fastapistatus.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": jsonable_encoder(exc.errors())},
        )
    except NotImplementedError:
        logger.debug(
            "NotImplementedError on applying pydantic schema to command"
        )
        return JSONResponse(
            status_code=fastapistatus.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Not implemented"},
        )

    try:
        if hasattr(command_data, "location_id"):
            location = await crud.get(
                ModuleID.locations,
                RoleEnum.cpo,
                command_data.location_id,
                auth_token=auth_token,
                version=VersionNumber.v_2_1_1,
            )
            if not location:
                raise NotFoundOCPIError

        command_response = await crud.do(
            ModuleID.commands,
            RoleEnum.cpo,
            Action.send_command,
            command_data.dict(),
            command=command,
            auth_token=auth_token,
            version=VersionNumber.v_2_1_1,
        )
        if command_response:
            if command_response["result"] == CommandResponseType.accepted:
                background_tasks.add_task(
                    send_command_result,
                    command_data=command_data,
                    command=command,
                    auth_token=auth_token,
                    crud=crud,
                    adapter=adapter,
                )
            return OCPIResponse(
                data=[
                    adapter.command_response_adapter(
                        command_response, VersionNumber.v_2_1_1
                    ).dict()
                ],
                **status.OCPI_1000_GENERIC_SUCESS_CODE,
            )

        logger.debug("Send command action returned without result.")
        command_response = CommandResponse(result=CommandResponseType.rejected)
        return OCPIResponse(
            data=[command_response.dict()],
            **status.OCPI_3000_GENERIC_SERVER_ERROR,
        )

    # when the location is not found
    except NotFoundOCPIError:
        logger.info(
            "Location with id `%s` was not found." % command_data.location_id
        )
        command_response = CommandResponse(result=CommandResponseType.rejected)
        return OCPIResponse(
            data=[command_response.dict()],
            **status.OCPI_2003_UNKNOWN_LOCATION,
        )
