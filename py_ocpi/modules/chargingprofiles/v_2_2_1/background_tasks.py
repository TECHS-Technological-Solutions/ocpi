import httpx

from asyncio import sleep

from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import encode_string_base64
from py_ocpi.core.config import settings
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core.config import logger
from py_ocpi.core.data_types import CiString, URL
from py_ocpi.core.enums import ModuleID, RoleEnum, Action

from py_ocpi.modules.chargingprofiles.v_2_2_1.schemas import (
    ChargingProfileResult,
    ChargingProfileResultType,
    SetChargingProfile,
)


async def send_get_chargingprofile(
    session_id: CiString(36),  # type: ignore
    duration: int,
    response_url: URL,
    auth_token: str,
    crud: Crud,
    adapter: Adapter,
):
    logger.info("Received command to send get chargingprofile request.")
    client_auth_token = await crud.do(
        ModuleID.charging_profile,
        RoleEnum.cpo,
        Action.get_client_token,
        auth_token=auth_token,
        version=VersionNumber.v_2_2_1,
    )

    active_charging_profile_result = None
    for _ in range(30 * settings.GET_ACTIVE_PROFILE_AWAIT_TIME):
        # since charging profile has no id, 0 is used for id parameter of crud.get
        active_charging_profile_result = await crud.get(
            ModuleID.hub_client_info,
            RoleEnum.cpo,
            0,
            session_id=session_id,
            duration=duration,
            response_url=response_url,
            auth_token=auth_token,
            version=VersionNumber.v_2_2_1,
        )
        if active_charging_profile_result:
            logger.debug(
                "Active charging profile result from Charge Point - %s"
                % active_charging_profile_result
            )
            break
        await sleep(2)

    if not active_charging_profile_result:
        logger.debug(
            "Active charging profile result from Charge Point "
            "didn't arrive in time."
        )
        active_charging_profile_result = ChargingProfileResult(
            result=ChargingProfileResultType.rejected
        )
    else:
        active_charging_profile_result = (
            adapter.active_charging_profile_result_adapter(
                active_charging_profile_result, VersionNumber.v_2_2_1
            )
        )

    async with httpx.AsyncClient() as client:
        authorization_token = f"Token {encode_string_base64(client_auth_token)}"
        logger.info(
            "Send request with active charging profile result: %s"
            % response_url
        )
        res = await client.post(
            response_url,
            json=active_charging_profile_result.dict(),
            headers={"authorization": authorization_token},
        )
        logger.info(
            "POST active chargingprofile result data after receiving result "
            "from Charge Point status_code: %s" % res.status_code
        )


async def send_update_chargingprofile(
    charging_profile: SetChargingProfile,
    session_id: CiString(36),  # type: ignore
    response_url: URL,
    auth_token: str,
    crud: Crud,
    adapter: Adapter,
):
    logger.info("Received command to send update chargingprofile request.")
    client_auth_token = await crud.do(
        ModuleID.charging_profile,
        RoleEnum.cpo,
        Action.get_client_token,
        auth_token=auth_token,
        version=VersionNumber.v_2_2_1,
    )

    charging_profile_result = None
    for _ in range(30 * settings.GET_ACTIVE_PROFILE_AWAIT_TIME):
        # since charging profile has no id, 0 is used for id parameter of crud.get
        charging_profile_result = await crud.get(
            ModuleID.hub_client_info,
            RoleEnum.cpo,
            0,
            session_id=session_id,
            response_url=response_url,
            charging_profile=charging_profile,
            auth_token=auth_token,
            version=VersionNumber.v_2_2_1,
        )
        if not charging_profile_result:
            logger.debug(
                "Charging profile result from Charge Point - %s"
                % charging_profile_result
            )
            break
        await sleep(2)

    if not charging_profile_result:
        logger.debug(
            "Charging profile result from Charge Point "
            "didn't arrive in time."
        )
        charging_profile_result = ChargingProfileResult(
            result=ChargingProfileResultType.rejected
        )
    else:
        charging_profile_result = (
            adapter.active_charging_profile_result_adapter(
                charging_profile_result, VersionNumber.v_2_2_1
            )
        )

    async with httpx.AsyncClient() as client:
        authorization_token = f"Token {encode_string_base64(client_auth_token)}"
        logger.info(
            "Send request with charging profile result: %s" % response_url
        )
        res = await client.post(
            response_url,
            json=charging_profile_result.dict(),
            headers={"authorization": authorization_token},
        )
        logger.info(
            "POST charging profile result data after receiving result "
            "from Charge Point status_code: %s" % res.status_code
        )


async def send_delete_chargingprofile(
    session_id: CiString(36),  # type: ignore
    response_url: URL,
    auth_token: str,
    crud: Crud,
    adapter: Adapter,
):
    logger.info("Received command to send delete chargingprofile request.")
    client_auth_token = await crud.do(
        ModuleID.charging_profile,
        RoleEnum.cpo,
        Action.get_client_token,
        auth_token=auth_token,
        version=VersionNumber.v_2_2_1,
    )

    clear_profile_result = None
    for _ in range(30 * settings.GET_ACTIVE_PROFILE_AWAIT_TIME):
        # since charging profile has no id, 0 is used for id parameter of crud.get
        clear_profile_result = await crud.get(
            ModuleID.hub_client_info,
            RoleEnum.cpo,
            0,
            session_id=session_id,
            response_url=response_url,
            auth_token=auth_token,
            version=VersionNumber.v_2_2_1,
        )
        if not clear_profile_result:
            logger.debug(
                "Clear profile result from Charge Point - %s"
                % clear_profile_result
            )
            break
        await sleep(2)

    if clear_profile_result:
        logger.debug(
            "Clear profile result from Charge Point " "didn't arrive in time."
        )
        clear_profile_result = ChargingProfileResult(
            result=ChargingProfileResultType.rejected
        )
    else:
        clear_profile_result = ChargingProfileResult(
            result=ChargingProfileResultType.accepted
        )

    async with httpx.AsyncClient() as client:
        authorization_token = f"Token {encode_string_base64(client_auth_token)}"
        logger.info("Send request with clear profile result: %s" % response_url)
        res = await client.post(
            response_url,
            json=clear_profile_result.dict(),
            headers={"authorization": authorization_token},
        )
        logger.info(
            "POST clear profile result data after receiving result "
            "from Charge Point status_code: %s" % res.status_code
        )
