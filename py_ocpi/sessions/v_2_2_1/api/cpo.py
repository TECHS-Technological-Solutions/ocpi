from fastapi import APIRouter, Depends, Response
from pydantic import ValidationError

from py_ocpi.sessions.v_2_2_1.schemas import ChargingPreferences
from py_ocpi.versions.enums import VersionNumber
from py_ocpi.core.utils import get_list
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID
from py_ocpi.core.dependencies import get_crud, get_adapter, pagination_filters

router = APIRouter(
    prefix='/sessions',
)


@router.get("/", response_model=OCPIResponse)
async def get_sessions(response: Response,
                       crud=Depends(get_crud),
                       adapter=Depends(get_adapter),
                       filters: dict = Depends(pagination_filters)):
    try:
        data_list = await get_list(response, filters, ModuleID.sessions,
                                   VersionNumber.v_2_2_1, crud)

        sessions = []
        for data in data_list:
            sessions.append(adapter.session_adapter(data).dict())
        return OCPIResponse(
            data=sessions,
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.put("/{session_id}/charging_preferences", response_model=OCPIResponse)
async def set_charging_preference(session_id: CiString(36),
                                  charging_preferences: ChargingPreferences,
                                  crud=Depends(get_crud),
                                  adapter=Depends(get_adapter)):
    data = await crud.update(ModuleID.sessions, charging_preferences.dict(), session_id)
    return OCPIResponse(
        data=adapter.charging_preference_adapter(data),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
