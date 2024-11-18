from enum import Enum


class ChargingProfileResultType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_charging_profiles.asciidoc#166-chargingprofileresulttype-enum
    """
    accepted = "ACCEPTED"
    rejected = "REJECTED"
    unknown = "UNKNOWN"


class ChargingProfileResponseType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_charging_profiles.asciidoc#165-chargingprofileresponsetype-enum
    """
    accepted = "ACCEPTED"
    not_supported = "NOT_SUPPORTED"
    rejected = "REJECTED"
    too_often = "TOO_OFTEN"
    unknown_session = "UNKNOWN_SESSION"


class ChargingRateUnit(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_charging_profiles.asciidoc#162-chargingrateunit-enum
    """
    watts = "W"
    amperes = "A"
