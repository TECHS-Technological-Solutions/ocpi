from fastapi import APIRouter, BackgroundTasks, Depends, Request

from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import get_auth_token
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.config import logger
from py_ocpi.core.data_types import CiString, URL
from py_ocpi.core.enums import ModuleID, RoleEnum, Action
from py_ocpi.core.dependencies import get_crud, get_adapter

from py_ocpi.modules.chargingprofiles.v_2_2_1.background_tasks import (
    send_get_chargingprofile,
    send_delete_chargingprofile,
    send_update_chargingprofile,
)
from py_ocpi.modules.chargingprofiles.v_2_2_1.schemas import (
    ChargingProfileResponse,
    ChargingProfileResponseType,
    SetChargingProfile,
)

router = APIRouter(
    prefix="/chargingprofiles",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_2_1))],
)


@router.get("/{session_id}", response_model=OCPIResponse)
async def get_chargingprofile(
    request: Request,
    session_id: CiString(36),  # type: ignore
    duration: int,
    response_url: URL,
    background_tasks: BackgroundTasks,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get Charging Profile.

    Retrieves the charging profile for a specific session.

    **Path parameters:**
        - session_id (str): The ID of the charging session.

    **Query parameters:**
        - duration (int): The requested duration for the charging profile.
        - response_url (URL): The URL to send the charging profile response.

    **Returns:**
        The OCPIResponse containing the charging profile response.

    **Raises:**
        - NotFoundOCPIError: If the specified charging session is not found.
    """
    logger.info(
        "Received request to get charging profile with session_id - `%s`."
        % session_id
    )
    auth_token = get_auth_token(request)

    session = await crud.get(
        ModuleID.sessions,
        RoleEnum.cpo,
        session_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_2_1,
    )

    if session:
        charging_profile_response = await crud.do(
            ModuleID.charging_profile,
            RoleEnum.cpo,
            Action.send_get_chargingprofile,
            session=session,
            duration=duration,
            response_url=response_url,
            auth_token=auth_token,
            version=VersionNumber.v_2_2_1,
        )

        if charging_profile_response:
            if (
                charging_profile_response["result"]
                == ChargingProfileResponseType.accepted
            ):
                background_tasks.add_task(
                    send_get_chargingprofile,
                    session_id=session_id,
                    duration=duration,
                    response_url=response_url,
                    auth_token=auth_token,
                    crud=crud,
                    adapter=adapter,
                )
            return OCPIResponse(
                data=[
                    adapter.charging_profile_response_adapter(
                        charging_profile_response
                    ).dict()
                ],
                **status.OCPI_1000_GENERIC_SUCESS_CODE,
            )

        logger.debug(
            "Sent get charging profile action returned without result."
        )
        charging_profile_response = ChargingProfileResponse(
            result=ChargingProfileResponseType.rejected, timeout=0
        )
        return OCPIResponse(
            data=[charging_profile_response.dict()],
            **status.OCPI_3000_GENERIC_SERVER_ERROR,
        )

    logger.info("Session with id `%s` was not found." % session_id)
    charging_profile_response = ChargingProfileResponse(
        result=ChargingProfileResponseType.rejected, timeout=0
    )
    return OCPIResponse(
        data=[charging_profile_response.dict()],
        **status.OCPI_2000_GENERIC_CLIENT_ERROR,
    )


@router.put("/{session_id}", response_model=OCPIResponse)
async def add_or_update_chargingprofile(
    request: Request,
    session_id: CiString(36),  # type: ignore
    charging_profile: SetChargingProfile,
    background_tasks: BackgroundTasks,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Add or Update Charging Profile.

    Adds or updates the charging profile for a specific session.

    **Path parameters:**
        - session_id (str): The ID of the charging session.

    **Request body:**
        - charging_profile (SetChargingProfile): The charging profile data.

    **Returns:**
        The OCPIResponse containing the charging profile response.

    **Raises:**
        - NotFoundOCPIError: If the specified charging session is not found.
    """
    logger.info(
        "Received request to get charging profile with session_id - `%s`."
        % session_id
    )
    logger.debug("Set charging profile data - `%s`" % charging_profile.dict())
    auth_token = get_auth_token(request)

    session = await crud.get(
        ModuleID.sessions,
        RoleEnum.cpo,
        session_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_2_1,
    )

    if session:
        charging_profile_response = await crud.do(
            ModuleID.charging_profile,
            RoleEnum.cpo,
            Action.send_update_charging_profile,
            charging_profile.dict(),
            session=session,
            response_url=charging_profile.response_url,
            auth_token=auth_token,
            version=VersionNumber.v_2_2_1,
        )

        if charging_profile_response:
            if (
                charging_profile_response["result"]
                == ChargingProfileResponseType.accepted
            ):
                background_tasks.add_task(
                    send_update_chargingprofile,
                    charging_profile=charging_profile,
                    session_id=session_id,
                    response_url=charging_profile.response_url,
                    auth_token=auth_token,
                    crud=crud,
                    adapter=adapter,
                )
            return OCPIResponse(
                data=[
                    adapter.charging_profile_response_adapter(
                        charging_profile_response
                    ).dict()
                ],
                **status.OCPI_1000_GENERIC_SUCESS_CODE,
            )

        logger.debug(
            "Sent update charging profile action returned without result."
        )
        charging_profile_response = ChargingProfileResponse(
            result=ChargingProfileResponseType.rejected, timeout=0
        )
        return OCPIResponse(
            data=[charging_profile_response.dict()],
            **status.OCPI_3000_GENERIC_SERVER_ERROR,
        )

    logger.info("Session with id `%s` was not found." % session_id)
    charging_profile_response = ChargingProfileResponse(
        result=ChargingProfileResponseType.rejected, timeout=0
    )
    return OCPIResponse(
        data=[charging_profile_response.dict()],
        **status.OCPI_2000_GENERIC_CLIENT_ERROR,
    )


@router.delete("/{session_id}", response_model=OCPIResponse)
async def delete_chargingprofile(
    request: Request,
    session_id: CiString(36),  # type: ignore
    response_url: URL,
    background_tasks: BackgroundTasks,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Delete Charging Profile.

    Deletes the charging profile for a specific session.

    **Path parameters:**
        - session_id (str): The ID of the charging session.

    **Query parameters:**
        - response_url (URL): The URL to send the response to.

    **Returns:**
        The OCPIResponse containing the charging profile response.

    **Raises:**
        - NotFoundOCPIError: If the specified charging session is not found.
    """
    logger.info(
        "Received request to get charging profile with session_id - `%s`."
        % session_id
    )
    auth_token = get_auth_token(request)

    session = await crud.get(
        ModuleID.sessions,
        RoleEnum.cpo,
        session_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_2_1,
    )

    if session:
        charging_profile_response = await crud.do(
            ModuleID.charging_profile,
            RoleEnum.cpo,
            Action.send_delete_chargingprofile,
            session=session,
            response_url=response_url,
            auth_token=auth_token,
            version=VersionNumber.v_2_2_1,
        )

        if charging_profile_response:
            if (
                charging_profile_response["result"]
                == ChargingProfileResponseType.accepted
            ):
                background_tasks.add_task(
                    send_delete_chargingprofile,
                    session_id=session_id,
                    response_url=response_url,
                    auth_token=auth_token,
                    crud=crud,
                    adapter=adapter,
                )
            return OCPIResponse(
                data=[
                    adapter.charging_profile_response_adapter(
                        charging_profile_response
                    ).dict()
                ],
                **status.OCPI_1000_GENERIC_SUCESS_CODE,
            )

        logger.debug(
            "Sent delete charging profile action returned without result."
        )
        charging_profile_response = ChargingProfileResponse(
            result=ChargingProfileResponseType.rejected, timeout=0
        )
        return OCPIResponse(
            data=[charging_profile_response.dict()],
            **status.OCPI_3000_GENERIC_SERVER_ERROR,
        )

    logger.info("Session with id `%s` was not found." % session_id)
    charging_profile_response = ChargingProfileResponse(
        result=ChargingProfileResponseType.rejected, timeout=0
    )
    return OCPIResponse(
        data=[charging_profile_response.dict()],
        **status.OCPI_2000_GENERIC_CLIENT_ERROR,
    )
