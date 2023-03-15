from asyncio import sleep

from fastapi import APIRouter, BackgroundTasks, Depends, Request, status as fastapistatus
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import httpx

from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core.enums import ModuleID, RoleEnum, Action
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core import status
from py_ocpi.core.utils import encode_string_base64, get_auth_token
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.commands.v_2_2_1.enums import CommandType
from py_ocpi.modules.commands.v_2_2_1.schemas import (
    CancelReservation, ReserveNow, StartSession,
    StopSession, UnlockConnector, CommandResult,
    CommandResultType, CommandResponse, CommandResponseType
)

router = APIRouter(
    prefix='/commands',
)


async def apply_pydantic_schema(command: str, data: dict):
    if command == CommandType.reserve_now:
        data = ReserveNow(**data)
    elif command == CommandType.cancel_reservation:
        data = CancelReservation(**data)
    elif command == CommandType.start_session:
        data = StartSession(**data)
    elif command == CommandType.stop_session:
        data = StopSession(**data)
    else:
        data = UnlockConnector(**data)
    return data


async def send_command_result(response_url: str, command: CommandType, auth_token: str, crud: Crud, adapter: Adapter):
    client_auth_token = await crud.do(ModuleID.commands, RoleEnum.cpo, Action.get_client_token,
                                      auth_token=auth_token, version=VersionNumber.v_2_2_1)

    for _ in range(150):  # check for 5 mins
        # since command has no id, 0 is used for id parameter of crud.get
        command_result = await crud.get(ModuleID.commands, RoleEnum.cpo, 0,
                                        auth_token=auth_token, version=VersionNumber.v_2_2_1, command=command)
        if command_result:
            break
        await sleep(2)

    if not command_result:
        command_result = CommandResult(result=CommandResultType.failed)
    else:
        command_result = adapter.command_result_adapter(command_result, VersionNumber.v_2_2_1)

    async with httpx.AsyncClient() as client:
        authorization_token = f'Token {encode_string_base64(client_auth_token)}'
        await client.post(response_url, json=command_result.dict(), headers={'authorization': authorization_token})


@router.post("/{command}", response_model=OCPIResponse)
async def receive_command(request: Request, command: CommandType, data: dict, background_tasks: BackgroundTasks,
                          crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    try:
        command_data = await apply_pydantic_schema(command, data)
    except ValidationError as exc:
        return JSONResponse(
            status_code=fastapistatus.HTTP_422_UNPROCESSABLE_ENTITY,
            content={'detail': jsonable_encoder(exc.errors())}
        )

    try:
        if hasattr(command_data, 'location_id'):
            await crud.get(ModuleID.locations, RoleEnum.cpo, command_data.location_id, auth_token=auth_token,
                           version=VersionNumber.v_2_2_1)

        command_response = await crud.do(ModuleID.commands, RoleEnum.cpo, Action.send_command, command_data.dict(),
                                         command=command, auth_token=auth_token, version=VersionNumber.v_2_2_1)

        background_tasks.add_task(send_command_result, response_url=command_data.response_url,
                                  command=command, auth_token=auth_token, crud=crud, adapter=adapter)

        return OCPIResponse(
            data=[adapter.command_response_adapter(command_response).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )

    # when the location is not found
    except NotFoundOCPIError:
        command_response = CommandResponse(result=CommandResponseType.rejected, timeout=0)
        return OCPIResponse(
            data=[command_response.dict()],
            **status.OCPI_2003_UNKNOWN_LOCATION,
        )
