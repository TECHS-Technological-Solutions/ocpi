from typing import List, Optional
from pydantic import BaseModel

from py_ocpi.cdrs.v_2_2_1.enums import AuthMethod
from py_ocpi.cdrs.v_2_2_1.schemas import CdrToken, ChargingPeriod
from py_ocpi.sessions.v_2_2_1.enums import ProfileType, SessionStatus
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


class ChargingPreferences(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_sessions.asciidoc#132-chargingpreferences-object
    """
    profile_type: ProfileType
    departure_time: Optional[DateTime]
    energy_need: Optional[Number]
    discharge_allowed: Optional[bool]
