from typing import List, Optional

from pydantic import BaseModel

from py_ocpi.locations.v_2_2_1.schemas import EnergyMix
from py_ocpi.tariffs.v_2_2_1.enums import DayOfWeek, ReservationRestrictionType, TariffDimensionType, TariffType
from py_ocpi.core.data_types import URL, CiString, DisplayText, Number, Price, String, DateTime


class PriceComponent(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#142-pricecomponent-class
    """
    type: TariffDimensionType
    price: Number
    vat: Optional[Number]
    step_size: int


class TariffRestrictions(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#146-tariffrestrictions-class
    """
    start_time: Optional[String(5)]
    end_time: Optional[String(5)]
    start_date: Optional[String(10)]
    end_date: Optional[String(10)]
    min_kwh: Optional[Number]
    max_kwh: Optional[Number]
    min_current: Optional[Number]
    max_current: Optional[Number]
    min_power: Optional[Number]
    max_power: Optional[Number]
    min_duration: Optional[int]
    max_duration: Optional[int]
    day_of_week: List[DayOfWeek] = []
    reservation: Optional[ReservationRestrictionType]


class TariffElement(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#144-tariffelement-class
    """
    price_components: List[PriceComponent]
    restrictions: Optional[TariffRestrictions]


class Tariff(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#131-tariff-object
    """
    country_code: CiString(2)
    party_id: CiString(3)
    id: CiString(36)
    currency: String(3)
    type: Optional[TariffType]
    tariff_alt_text: List[DisplayText] = []
    tariff_alt_url: Optional[URL]
    min_price: Optional[Price]
    max_price: Optional[Price]
    elements: List[TariffElement]
    start_date_time: Optional[DateTime]
    end_date_time: Optional[DateTime]
    energy_mix: Optional[EnergyMix]
    last_updated: DateTime
