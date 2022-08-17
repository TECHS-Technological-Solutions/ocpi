from typing import List, Optional
from pydantic import BaseModel

from py_ocpi.tokens.v_2_2_1.enums import TokenType
from py_ocpi.locations.v_2_2_1.enums import (
    EnergySourceCategory, ParkingType, ParkingRestriction, Facility, Status, Capability,
    ConnectorFormat, ConnectorType, PowerType, ImageCategory, EnvironmentalImpactCategory
)
from py_ocpi.core.data_types import URL, CiString, DisplayText, Number, String, DateTime


class PublishTokenType(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_publish_token_class
    """
    uid: Optional[CiString(max_length=36)]
    type: Optional[TokenType]
    visual_number: Optional[String(max_length=64)]
    issuer: Optional[String(max_length=64)]
    group_id: Optional[CiString(max_length=36)]


class Image(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1415-image-class
    """
    url: URL
    thumbnail: Optional[URL]
    category: ImageCategory
    type: CiString(max_length=4)
    width: Optional[int]
    height: Optional[int]


class GeoLocation(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_geolocation_class
    """
    latitude: String(max_length=10)
    longitude: String(max_length=11)


class AdditionalGeoLocation(GeoLocation):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_additionalgeolocation_class
    """
    name: Optional[DisplayText]


class Connector(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#133-connector-object
    """
    id: CiString(max_length=36)
    standard: ConnectorType
    format: ConnectorFormat
    power_type: PowerType
    max_voltage: int
    max_amperage: int
    max_electric_power: Optional[int]
    tariff_ids: List[CiString(max_length=36)] = []
    terms_and_conditions: Optional[URL]
    last_updated: DateTime


class StatusSchedule(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1423-statusschedule-class
    """
    period_begin: DateTime
    period_end: Optional[DateTime]
    status: Status


class EVSE(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_evse_object
    """
    uid: CiString(max_length=36)
    evse_id: Optional[CiString(max_length=48)]
    status: Status
    status_schedule: Optional[StatusSchedule]
    capabilities: List[Capability] = []
    connectors: List[Connector]
    floor_level: Optional[String(max_length=4)]
    coordinates: Optional[GeoLocation]
    physical_reference: Optional[String(max_length=16)]
    directions: List[DisplayText] = []
    parking_restrictions: List[ParkingRestriction] = []
    images: List[Image] = []
    last_updated: DateTime


class BusinessDetails(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_businessdetails_class
    """
    name: String(max_length=100)
    website: Optional[URL]
    logo: Optional[Image]


class RegularHours(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1421-regularhours-class
    """
    weekday: int
    period_begin: String(max_length=5)
    period_end: String(max_length=5)


class ExceptionalPeriod(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1411-exceptionalperiod-class
    """
    period_begin: DateTime
    period_end: DateTime


class Hours(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_hours_class
    """
    twentyfourseven: bool
    regular_hours: List[RegularHours]
    exceptional_openings: List[ExceptionalPeriod] = []
    exceptional_closings: List[ExceptionalPeriod] = []


class EnergySource(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#147-energysource-class
    """
    source: EnergySourceCategory
    percentage: Number


class EnvironmentalImpact(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#149-environmentalimpact-class
    """
    category: EnvironmentalImpactCategory
    amount: Number


class EnergyMix(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#mod_locations_energymix_class
    """
    is_green_energy: bool
    energy_sources: List[EnergySource]
    environ_impact: Optional[EnvironmentalImpact]
    supplier_name: String(max_length=64)
    energy_product_name: String(max_length=64)


class Location(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#131-location-object
    """
    country_code: CiString(max_length=2)
    party_id: CiString(max_length=3)
    id: CiString(max_length=36)
    publish: bool
    publish_allowed_to: List[PublishTokenType] = []
    name: Optional[String(max_length=255)]
    address: String(max_length=45)
    city: String(max_length=45)
    postal_code: Optional[String(max_length=10)]
    state: Optional[String(max_length=20)]
    country: String(max_length=3)
    coordinates: GeoLocation
    related_locations: List[AdditionalGeoLocation] = []
    parking_type: Optional[ParkingType]
    evses: List[EVSE] = []
    directions: List[DisplayText] = []
    operator: Optional[BusinessDetails]
    suboperator: Optional[BusinessDetails]
    owner: Optional[BusinessDetails]
    facilities: List[Facility] = []
    time_zone: String(max_length=255)
    opening_times: Optional[Hours]
    charging_when_closed: Optional[bool]
    images: List[Image] = []
    energy_mix: Optional[EnergyMix]
    last_updated: DateTime
