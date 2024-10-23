from fastapi import APIRouter, Depends, Response, Request

from py_ocpi.modules.sessions.v_2_2_1.schemas import ChargingPreferences
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import get_list, get_auth_token
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.config import logger
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.dependencies import get_crud, get_adapter, pagination_filters

router = APIRouter(
    prefix="/sessions",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_2_1))],
)


@router.get("/", response_model=OCPIResponse)
async def get_sessions(
    request: Request,
    response: Response,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    filters: dict = Depends(pagination_filters),
):
    """
    Get sessions.

    Retrieves a list of sessions based on the specified filters.

    **Query parameters:**
       - limit (int): Maximum number of objects to GET (default=50).
       - offset (int): The offset of the first object returned (default=0).
       - date_from (datetime): Only return Sessions that have last_updated
            after this Date/Time (default=None).
       - date_to (datetime): Only return Sessions that have last_updated
            before this Date/Time (default=None).

    **Returns:**
       The OCPIResponse containing the list of CDRs.
    """
    logger.info("Received request to get sessions.")
    auth_token = get_auth_token(request)

    data_list = await get_list(
        response,
        filters,
        ModuleID.sessions,
        RoleEnum.cpo,
        VersionNumber.v_2_2_1,
        crud,
        auth_token=auth_token,
    )

    sessions = []
    for data in data_list:
        sessions.append(adapter.session_adapter(data).dict())
    logger.debug(f"Amount of sessions in response: {len(sessions)}")
    return OCPIResponse(
        data=sessions,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.put("/{session_id}/charging_preferences", response_model=OCPIResponse)
async def set_charging_preference(
    request: Request,
    session_id: CiString(36),  # type: ignore
    charging_preferences: ChargingPreferences,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Set Charging Preference.

    Updates the charging preference for a specific charging session.

    **Path parameters:**
        - session_id (str): The ID of the charging session (36 characters).

    **Request body:**
        charging_preferences (ChargingPreferences): The charging preferences
            object.

    **Returns:**
        The OCPIResponse containing the updated charging preferences.
    """
    auth_token = get_auth_token(request)
    data = await crud.update(
        ModuleID.sessions,
        RoleEnum.cpo,
        charging_preferences.dict(),
        session_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_2_1,
    )
    return OCPIResponse(
        data=[adapter.charging_preference_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
