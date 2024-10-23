from typing import List, Optional

from pydantic import BaseModel

from py_ocpi.core.data_types import URL, DisplayText, Number, String, DateTime
from py_ocpi.modules.locations.v_2_1_1.schemas import EnergyMix
from py_ocpi.modules.tariffs.v_2_1_1.enums import (
    DayOfWeek,
    TariffDimensionType,
)


class PriceComponent(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tariffs.md#42-pricecomponent-class
    """

    type: TariffDimensionType
    price: Number
    step_size: int


class TariffRestrictions(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tariffs.md#45-tariffrestrictions-class
    """

    start_time: Optional[String(5)]  # type: ignore
    end_time: Optional[String(5)]  # type: ignore
    start_date: Optional[String(10)]  # type: ignore
    end_date: Optional[String(10)]  # type: ignore
    min_kwh: Optional[Number]
    max_kwh: Optional[Number]
    min_power: Optional[Number]
    max_power: Optional[Number]
    min_duration: Optional[int]
    max_duration: Optional[int]
    day_of_week: List[DayOfWeek] = []


class TariffElement(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tariffs.md#43-tariffelement-class
    """

    price_components: List[PriceComponent]
    restrictions: Optional[TariffRestrictions]


class Tariff(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tariffs.md#31-tariff-object
    """

    id: String(36)  # type: ignore
    currency: String(3)  # type: ignore
    tariff_alt_text: List[DisplayText] = []
    tariff_alt_url: Optional[URL]
    elements: List[TariffElement]
    energy_mix: Optional[EnergyMix]
    last_updated: DateTime


class TariffPartialUpdate(BaseModel):
    id: Optional[String(36)]  # type: ignore
    currency: Optional[String(3)]  # type: ignore
    tariff_alt_text: Optional[List[DisplayText]]
    tariff_alt_url: Optional[URL]
    elements: Optional[List[TariffElement]]
    energy_mix: Optional[EnergyMix]
    last_updated: Optional[DateTime]
