from typing import Optional
from pydantic import BaseModel

from py_ocpi.core.data_types import String, URL, DateTime
from py_ocpi.modules.commands.v_2_1_1.enums import CommandResponseType
from py_ocpi.modules.tokens.v_2_1_1.schemas import Token


class CommandResponse(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_commands.md#31-commandresponse-object
    """

    result: CommandResponseType


class ReserveNow(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_commands.md#32-reservenow-object
    """

    response_url: URL
    token: Token
    expiry_date: DateTime
    reservation_id: int
    location_id: String(36)  # type: ignore
    evse_uid: Optional[String(39)]  # type: ignore


class StartSession(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_commands.md#33-startsession-object
    """

    response_url: URL
    token: Token
    location_id: String(39)  # type: ignore
    evse_uid: Optional[String(39)]  # type: ignore


class StopSession(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_commands.md#34-stopsession-object
    """

    response_url: URL
    session_id: String(36)  # type: ignore


class UnlockConnector(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_commands.md#35-unlockconnector-object
    """

    response_url: URL
    location_id: String(39)  # type: ignore
    evse_uid: String(39)  # type: ignore
    connector_id: String(39)  # type: ignore
