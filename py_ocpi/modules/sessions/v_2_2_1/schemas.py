from typing import List, Optional
from pydantic import BaseModel, validator

from py_ocpi.modules.cdrs.v_2_2_1.enums import AuthMethod
from py_ocpi.modules.cdrs.v_2_2_1.schemas import CdrToken, ChargingPeriod
from py_ocpi.modules.sessions.v_2_2_1.enums import ProfileType, SessionStatus
from py_ocpi.core.data_types import CiString, Number, Price, String, DateTime


class Session(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_sessions.asciidoc#131-session-object
    """
    country_code: CiString(2)
    party_id: CiString(3)
    id: CiString(36)
    start_date_time: DateTime
    end_date_time: Optional[DateTime]
    kwh: Number
    cdr_token: CdrToken
    auth_method: AuthMethod
    authorization_reference: Optional[CiString(36)]
    location_id: CiString(36)
    evse_uid: CiString(36)
    connector_id: CiString(36)
    meter_id: Optional[String(255)]
    currency: String(3)
    charging_periods: List[ChargingPeriod] = []
    total_cost: Optional[Price]
    status: SessionStatus
    last_updated: DateTime

    @validator('country_code')
    def country_code_to_upper(cls, v):
        return v.upper()
    
    @validator('party_id')
    def party_id_to_upper(cls, v):
        return v.upper()


class SessionPartialUpdate(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_sessions.asciidoc#131-session-object
    """
    country_code: Optional[CiString(2)]
    party_id: Optional[CiString(3)]
    id: Optional[CiString(36)]
    start_date_time: Optional[DateTime]
    end_date_time: Optional[DateTime]
    kwh: Optional[Number]
    cdr_token: Optional[CdrToken]
    auth_method: Optional[AuthMethod]
    authorization_reference: Optional[CiString(36)]
    location_id: Optional[CiString(36)]
    evse_uid: Optional[CiString(36)]
    connector_id: Optional[CiString(36)]
    meter_id: Optional[String(255)]
    currency: Optional[String(3)]
    charging_periods: Optional[List[ChargingPeriod]]
    total_cost: Optional[Price]
    status: Optional[SessionStatus]
    last_updated: Optional[DateTime]


class ChargingPreferences(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_sessions.asciidoc#132-chargingpreferences-object
    """
    profile_type: ProfileType
    departure_time: Optional[DateTime]
    energy_need: Optional[Number]
    discharge_allowed: Optional[bool]
