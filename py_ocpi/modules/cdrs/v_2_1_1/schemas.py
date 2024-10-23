from typing import List, Optional

from pydantic import BaseModel
from py_ocpi.modules.cdrs.v_2_1_1.enums import (
    AuthMethod,
    CdrDimensionType,
)

from py_ocpi.core.data_types import CiString, Number, String, DateTime
from py_ocpi.modules.locations.v_2_1_1.schemas import Location
from py_ocpi.modules.tariffs.v_2_1_1.schemas import Tariff


class CdrDimension(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_cdrs.md#42-cdrdimension-class
    """

    type: CdrDimensionType
    volume: Number


class ChargingPeriod(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_cdrs.md#44-chargingperiod-class
    """

    start_date_time: DateTime
    dimensions: List[CdrDimension]


class Cdr(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_cdrs.md#31-cdr-object
    """

    id: CiString(36)  # type: ignore
    start_date_time: DateTime
    end_date_time: DateTime
    auth_id: String(36)  # type: ignore
    auth_method: AuthMethod
    location: Location
    meter_id: Optional[String(255)]  # type: ignore
    currency: String(3)  # type: ignore
    tariffs: List[Tariff] = []
    charging_periods: List[ChargingPeriod]
    total_cost: Number
    total_energy: Number
    total_time: Number
    total_parking_time: Optional[Number]
    remark: Optional[String(255)]  # type: ignore
    last_updated: DateTime
