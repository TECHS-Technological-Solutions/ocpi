from fastapi import APIRouter, Depends, Request, status as fastapistatus
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core.enums import ModuleID, RoleEnum, Action
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core import status
from py_ocpi.core.utils import get_auth_token
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.commands.v_2_2_1.enums import CommandType
from py_ocpi.modules.commands.v_2_2_1.schemas import (
    CancelReservation, ReserveNow, StartSession,
    StopSession, UnlockConnector
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


@router.post("/{command}", response_model=OCPIResponse)
async def receive_command(request: Request, command: CommandType, data: dict,
                          crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    try:
        data = await apply_pydantic_schema(command, data)
    except ValidationError as exc:
        return JSONResponse(
            status_code=fastapistatus.HTTP_422_UNPROCESSABLE_ENTITY,
            content={'detail': jsonable_encoder(exc.errors())}
        )
    try:
        data = await crud.do(ModuleID.commands, RoleEnum.cpo, Action.send_command, data.dict(), command=command,
                             auth_token=auth_token, version=VersionNumber.v_2_2_1)
        return OCPIResponse(
            data=[adapter.commands_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )
