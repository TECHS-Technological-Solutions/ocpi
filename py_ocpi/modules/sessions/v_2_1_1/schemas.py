from typing import List, Optional
from pydantic import BaseModel

from py_ocpi.core.data_types import Number, Price, String, DateTime
from py_ocpi.modules.cdrs.v_2_1_1.enums import AuthMethod
from py_ocpi.modules.cdrs.v_2_1_1.schemas import ChargingPeriod
from py_ocpi.modules.locations.v_2_1_1.schemas import Location
from py_ocpi.modules.sessions.v_2_1_1.enums import SessionStatus


class Session(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_sessions.md#31-session-object
    """

    id: String(36)  # type: ignore
    start_datetime: DateTime
    end_datetime: Optional[DateTime]
    kwh: Number
    auth_id: String(36)  # type: ignore
    auth_method: AuthMethod
    location: Location
    meter_id: Optional[String(255)]  # type: ignore
    currency: String(3)  # type: ignore
    charging_periods: List[ChargingPeriod] = []
    total_cost: Optional[Price]
    status: SessionStatus
    last_updated: DateTime


class SessionPartialUpdate(BaseModel):
    id: Optional[String(36)]  # type: ignore
    start_datetime: Optional[DateTime]
    end_datetime: Optional[DateTime]
    kwh: Optional[Number]
    auth_id: Optional[String(36)]  # type: ignore
    auth_method: Optional[AuthMethod]
    location: Optional[Location]
    meter_id: Optional[String(255)]  # type: ignore
    currency: Optional[String(3)]  # type: ignore
    charging_periods: Optional[List[ChargingPeriod]]
    total_cost: Optional[Price]
    status: Optional[SessionStatus]
    last_updated: Optional[DateTime]
