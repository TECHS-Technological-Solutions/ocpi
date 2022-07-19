from typing import List
from pydantic import BaseModel, validator

from tokens.v_2_2_1.enums import TokenType
from locations.v_2_2_1.enums import (
    EnergySourceCategory, ParkingType, ParkingRestriction, Facility, Status, Capability,
    ConnectorFormat, ConnectorType, PowerType, ImageCategory, EnvironmentalImpactCategory
)
from ocpi.core.v_2_2_1.data_types import URL, CiString, DisplayText, Number, String, DateTime


def length_validator(field: str, string: str, length: int):
    if len(string) > length:
        raise ValueError('%s length must be lower or equal to %s', field, length)


class PublishTokenType(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#mod_locations_publish_token_class
    """
    uid: CiString
    type: TokenType
    visual_number: String
    issuer: String
    group_id: CiString

    @validator('uid')
    def validate_uid(cls, v):
        length_validator('uid', v, 36)
        return v

    @validator('visual_number')
    def validate_visual_number(cls, v):
        length_validator('visual_number', v, 64)
        return v

    @validator('issuer')
    def validate_issuer(cls, v):
        length_validator('issuer', v, 64)
        return v

    @validator('group_id')
    def validate_group_id(cls, v):
        length_validator('group_id', v, 36)
        return v


class Image(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#1415-image-class
    """
    url: URL
    thumbnail: URL
    category: ImageCategory
    type: CiString
    width: int
    height: int

    @validator('type')
    def validate_type(cls, v):
        length_validator('type', v, 4)
        return v


class GeoLocation(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#mod_locations_geolocation_class
    """
    latitude: String
    longitude: String

    @validator('latitude')
    def validate_latitude(cls, v):
        length_validator('latitude', v, 10)
        return v

    @validator('longitude')
    def validate_longitude(cls, v):
        length_validator('longitude', v, 11)
        return v


class AdditionalGeoLocation(GeoLocation):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#mod_locations_additionalgeolocation_class
    """
    name: DisplayText


class Connector(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#133-connector-object
    """
    id: CiString
    standard: ConnectorType
    format: ConnectorFormat
    power_type: PowerType
    max_voltage: int
    max_amperage: int
    max_electric_power: int
    tariff_ids: CiString
    terms_and_conditions: URL
    last_updated: DateTime

    @validator('id')
    def validate_id(cls, v):
        length_validator('id', v, 36)
        return v

    @validator('tariff_ids')
    def validate_tariff_ids(cls, v):
        length_validator('tariff_ids', v, 36)
        return v


class StatusSchedule(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#1423-statusschedule-class
    """
    period_begin: DateTime
    period_end: DateTime
    status: Status


class EVSE(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#mod_locations_evse_object
    """
    uid: CiString
    evse_id: CiString
    status: Status
    status_schedule: StatusSchedule
    capabilities: List[Capability]
    connectors: List[Connector]
    floor_level: String
    coordinates: GeoLocation
    physical_reference: String
    directions: DisplayText
    parking_restrictions: ParkingRestriction
    images: Image
    last_updated: DateTime

    @validator('uid')
    def validate_uid(cls, v):
        length_validator('uid', v, 36)
        return v

    @validator('evse_id')
    def validate_evse_id(cls, v):
        length_validator('evse_id', v, 48)
        return v

    @validator('floor_level')
    def validate_floor_level(cls, v):
        length_validator('floor_level', v, 4)
        return v

    @validator('physical_reference')
    def validate_id(cls, v):
        length_validator('physical_reference', v, 16)
        return v


class BusinessDetails(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#mod_locations_businessdetails_class
    """
    name: String
    website: URL
    logo: Image

    @validator('name')
    def validate_name(cls, v):
        length_validator('name', v, 100)
        return v


class RegularHours(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#1421-regularhours-class
    """
    weekday: int
    period_begin: String
    period_end: String


class ExceptionalPeriod(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#1411-exceptionalperiod-class
    """
    period_begin: DateTime
    period_end: DateTime


class Hours(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#mod_locations_hours_class
    """
    twentyfourseven: bool
    regular_hours: RegularHours
    exceptional_openings: ExceptionalPeriod
    exceptional_closings: ExceptionalPeriod


class EnergySource(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#147-energysource-class
    """
    source: EnergySourceCategory
    percentage: Number


class EnvironmentalImpact(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#149-environmentalimpact-class
    """
    category: EnvironmentalImpactCategory
    amount: Number


class EnergyMix(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#mod_locations_energymix_class
    """
    is_green_energy: bool
    energy_source: EnergySource
    environ_impact: EnvironmentalImpact
    supplier_name: String
    energy_product_name: String

    @validator('supplier_name')
    def validate_supplier_name(cls, v):
        length_validator('supplier_name', v, 64)
        return v

    @validator('energy_product_name')
    def validate_energy_product_name(cls, v):
        length_validator('energy_product_name', v, 64)
        return v


class Location(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_locations.asciidoc#131-location-object
    """
    country_code: CiString
    party_id: CiString
    id: CiString
    publish: bool
    publish_allowed_to: PublishTokenType
    name: String
    address: String
    city: String
    postal_code: String
    state: String
    country: String
    coordinates: GeoLocation
    related_locations: AdditionalGeoLocation
    parking_type: ParkingType
    evses: List[EVSE]
    directions: DisplayText
    operator: BusinessDetails
    suboperator: BusinessDetails
    owner: BusinessDetails
    facilities: Facility
    time_zone: String
    opening_times: Hours
    charging_when_closed: bool
    images: Image
    energy_mix: EnergyMix
    last_updated: DateTime

    @validator('country_code')
    def validate_country_code(cls, v):
        length_validator('country_code', v, 2)
        return v

    @validator('party_id')
    def validate_party_id(cls, v):
        length_validator('party_id', v, 3)
        return v

    @validator('id')
    def validate_id(cls, v):
        length_validator('id', v, 36)
        return v

    @validator('name')
    def validate_name(cls, v):
        length_validator('name', v, 255)
        return v

    @validator('address')
    def validate_address(cls, v):
        length_validator('address', v, 45)
        return v

    @validator('city')
    def validate_city(cls, v):
        length_validator('city', v, 45)
        return v

    @validator('postal_code')
    def validate_postal_code(cls, v):
        length_validator('postal_code', v, 10)
        return v

    @validator('state')
    def validate_state(cls, v):
        length_validator('state', v, 20)
        return v

    @validator('country')
    def validate_country(cls, v):
        length_validator('country', v, 3)
        return v

    @validator('time_zone')
    def validate_time_zone(cls, v):
        length_validator('time_zone', v, 255)
        return v
