from typing import List, Optional
from pydantic import BaseModel, validator

from py_ocpi.core.data_types import CiString, URL, DisplayText, DateTime
from py_ocpi.locations.v_2_2_1.schemas import length_validator
from py_ocpi.commands.v_2_2_1.enums import CommandResponseType, CommandResultType
from py_ocpi.tokens.v_2_2_1.schemas import Token


class CancelReservation(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_commands.asciidoc#131-cancelreservation-object
    """
    response_url: URL
    reservation_id: CiString

    @validator('reservation_id')
    def validate_reservation_id(cls, v):
        length_validator('reservation_id', v, 36)
        return v


class CommandResponse(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_commands.asciidoc#132-commandresponse-object
    """
    result: CommandResponseType
    timeout: int
    message: List[DisplayText] = []


class CommandResult(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_commands.asciidoc#133-commandresult-object
    """
    result: CommandResultType
    message: List[DisplayText] = []


class ReserveNow(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_commands.asciidoc#134-reservenow-object
    """
    response_url: URL
    token: Token
    expiry_date: DateTime
    reservation_id: CiString
    location_id: CiString
    evse_uid: Optional[CiString]
    authorization_reference: Optional[CiString]

    @validator('reservation_id')
    def validate_reservation_id(cls, v):
        length_validator('reservation_id', v, 36)
        return v

    @validator('location_id')
    def validate_location_id(cls, v):
        length_validator('location_id', v, 36)
        return v

    @validator('evse_uid')
    def validate_evse_uid(cls, v):
        length_validator('evse_uid', v, 36)
        return v

    @validator('authorization_reference')
    def validate_authorization_reference(cls, v):
        length_validator('authorization_reference', v, 36)
        return v


class StartSession(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_commands.asciidoc#135-startsession-object
    """
    response_url: URL
    token: Token
    location_id: CiString
    evse_uid: Optional[CiString]
    connector_id: Optional[CiString]
    authorization_reference: Optional[CiString]

    @validator('location_id')
    def validate_location_id(cls, v):
        length_validator('location_id', v, 36)
        return v

    @validator('evse_uid')
    def validate_evse_uid(cls, v):
        length_validator('evse_uid', v, 36)
        return v

    @validator('connector_id')
    def validate_connector_id(cls, v):
        length_validator('connector_id', v, 36)
        return v

    @validator('authorization_reference')
    def validate_authorization_reference(cls, v):
        length_validator('authorization_reference', v, 36)
        return v


class StopSession(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_commands.asciidoc#136-stopsession-object
    """
    response_url: URL
    session_id: CiString

    @validator('session_id')
    def validate_session_id(cls, v):
        length_validator('session_id', v, 36)
        return v


class UnlockConnector(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_commands.asciidoc#137-unlockconnector-object
    """
    response_url: URL
    location_id: CiString
    evse_uid: CiString
    connector_id: CiString

    @validator('location_id')
    def validate_location_id(cls, v):
        length_validator('location_id', v, 36)
        return v

    @validator('evse_uid')
    def validate_evse_uid(cls, v):
        length_validator('evse_uid', v, 36)
        return v

    @validator('connector_id')
    def validate_connector_id(cls, v):
        length_validator('connector_id', v, 36)
        return v
