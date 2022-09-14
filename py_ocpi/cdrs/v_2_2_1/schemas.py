from typing import List, Optional

from pydantic import BaseModel
from py_ocpi.cdrs.v_2_2_1.enums import AuthMethod, CdrDimensionType

from py_ocpi.core.data_types import CiString, Number, Price, String, DateTime
from py_ocpi.tokens.v_2_2_1.enums import TokenType
from py_ocpi.tariffs.v_2_2_1.schemas import Tariff
from py_ocpi.locations.v_2_2_1.schemas import GeoLocation
from py_ocpi.locations.v_2_2_1.enums import ConnectorFormat, ConnectorType, PowerType


class SignedValue(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#148-signedvalue-class
    """
    nature: CiString(32)
    plain_data: String(512)
    singed_data: String(5000)


class SignedData(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#147-signeddata-class
    """
    encoding_method: CiString(36)
    encoding_method_version: Optional[int]
    public_key: Optional[String(512)]
    signed_value: List[SignedValue]
    url: Optional[String(512)]


class CdrDimension(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#142-cdrdimension-class
    """
    type: CdrDimensionType
    volume: Number


class ChargingPeriod(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#146-chargingperiod-class
    """
    start_date_time: DateTime
    diemnsions: List[CdrDimension]
    tariff_id: Optional[CiString(36)]


class CdrToken(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#145-cdrtoken-class
    """
    country_code: CiString(2)
    party_id: CiString(3)
    uid: CiString(36)
    type: TokenType
    contract_id: CiString(36)


class CdrLocation(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#144-cdrlocation-class
    """
    id: CiString(36)
    name: Optional[String(255)]
    address: String(45)
    city: String(45)
    postal_code: Optional[String(10)]
    state: Optional[String(20)]
    country: String(3)
    coordinates: GeoLocation
    evse_id: CiString(48)
    connector_id: CiString(36)
    connector_standard: ConnectorType
    connector_format: ConnectorFormat
    connector_power_type: PowerType


class Cdr(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#131-cdr-object
    """
    country_code: CiString(2)
    party_id: CiString(3)
    id: CiString(39)
    start_date_time: DateTime
    end_date_time: DateTime
    session_id: Optional[CiString(36)]
    cdr_token: CdrToken
    auth_method: AuthMethod
    authorization_reference: Optional[CiString(36)]
    cdr_location: CdrLocation
    meter_id: Optional[String(255)]
    currency: String(3)
    tariffs: List[Tariff] = []
    charging_periods: List[ChargingPeriod]
    signed_data: Optional[SignedData]
    total_cost: Price
    total_fixed_cost: Optional[Price]
    total_energy: Number
    total_energy_cost: Optional[Price]
    total_time: Number
    total_time_cost: Optional[Price]
    total_parking_time: Optional[Number]
    total_parking_cost: Optional[Price]
    total_reservation_cost: Optional[Price]
    remark: Optional[String(255)]
    invoice_reference_id: Optional[CiString(36)]
    credit: Optional[bool]
    credit_reference_id: Optional[CiString(39)]
    home_charging_compensation: Optional[bool]
    last_updated: DateTime
