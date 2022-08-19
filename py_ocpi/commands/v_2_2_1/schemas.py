from typing import List, Optional
from pydantic import BaseModel

from py_ocpi.core.data_types import CiString, URL, DisplayText, DateTime
from py_ocpi.commands.v_2_2_1.enums import CommandResponseType, CommandResultType
from py_ocpi.tokens.v_2_2_1.schemas import Token


class CancelReservation(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_commands.asciidoc#131-cancelreservation-object
    """
    response_url: URL
    reservation_id: CiString(36)


class CommandResponse(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_commands.asciidoc#132-commandresponse-object
    """
    result: CommandResponseType
    timeout: int
    message: List[DisplayText] = []


class CommandResult(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_commands.asciidoc#133-commandresult-object
    """
    result: CommandResultType
    message: List[DisplayText] = []


class ReserveNow(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_commands.asciidoc#134-reservenow-object
    """
    response_url: URL
    token: Token
    expiry_date: DateTime
    reservation_id: CiString(36)
    location_id: CiString(36)
    evse_uid: Optional[CiString(36)]
    authorization_reference: Optional[CiString(36)]


class StartSession(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_commands.asciidoc#135-startsession-object
    """
    response_url: URL
    token: Token
    location_id: CiString(36)
    evse_uid: Optional[CiString(36)]
    connector_id: Optional[CiString(36)]
    authorization_reference: Optional[CiString(36)]


class StopSession(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_commands.asciidoc#136-stopsession-object
    """
    response_url: URL
    session_id: CiString(36)


class UnlockConnector(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_commands.asciidoc#137-unlockconnector-object
    """
    response_url: URL
    location_id: CiString(36)
    evse_uid: CiString(36)
    connector_id: CiString(36)
