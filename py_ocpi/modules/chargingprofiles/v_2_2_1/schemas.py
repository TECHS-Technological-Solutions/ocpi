from typing import Optional
from pydantic import BaseModel

from py_ocpi.core.data_types import DateTime, Number, URL
from py_ocpi.modules.chargingprofiles.v_2_2_1.enums import (
    ChargingProfileResponseType,
    ChargingProfileResultType,
    ChargingRateUnit,
)


class ChargingProfilePeriod(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_charging_profiles.asciidoc#164-chargingprofileperiod-class
    """

    start_period: int
    limit: Number


class ChargingProfile(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_charging_profiles.asciidoc#163-chargingprofile-class
    """

    start_date_time: Optional[DateTime]
    duration: Optional[int]
    charging_rate_unit: ChargingRateUnit
    min_charge_rate: Number
    charging_profile_period: ChargingProfilePeriod


class ActiveChargingProfile(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_charging_profiles.asciidoc#161-activechargingprofile-class
    """

    start_date_time: DateTime
    charging_profile: ChargingProfile


class ChargingProfileResponse(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_charging_profiles.asciidoc#151-chargingprofileresponse-object
    """

    result: ChargingProfileResponseType
    timeout: int


class ActiveChargingProfileResult(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_charging_profiles.asciidoc#152-activechargingprofileresult-object
    """

    result: ChargingProfileResultType
    profile: Optional[ActiveChargingProfile]


class ChargingProfileResult(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_charging_profiles.asciidoc#153-chargingprofileresult-object
    """

    result: ChargingProfileResultType


class ClearProfileResult(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_charging_profiles.asciidoc#154-clearprofileresult-object
    """

    result: ChargingProfileResultType


class SetChargingProfile(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_charging_profiles.asciidoc#155-setchargingprofile-object
    """

    charging_profile: ChargingProfile
    response_url: URL
