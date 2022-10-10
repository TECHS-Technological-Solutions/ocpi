from typing import Union

from fastapi import APIRouter, Depends, Request
from pydantic import ValidationError

from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core.enums import ModuleID
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core import status
from py_ocpi.core.utils import get_auth_token
from py_ocpi.commands.v_2_2_1.enums import CommandType
from py_ocpi.commands.v_2_2_1.schemas import CancelReservation, ReserveNow, StartSession, StopSession, UnlockConnector

router = APIRouter(
    prefix='/commands',
)


@router.post("/{command}", response_model=OCPIResponse)
async def receive_command(request: Request, command: CommandType,
                          data: Union[CancelReservation, ReserveNow, StartSession, StopSession, UnlockConnector],
                          crud=Depends(get_crud), adapter=Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        response = await crud.create(ModuleID.commands, data.dict(), command=command, auth_token=auth_token)
        return OCPIResponse(
            data=[adapter.commands_adapter(response)],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )
