from enum import Enum


class AuthMethod(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_cdrs.md#41-authmethod-enum
    """

    # Authentication request from the eMSP
    auth_request = "AUTH_REQUEST"
    # Whitelist used to authenticate, no request done to the eMSP
    whitelist = "WHITELIST"


class CdrDimensionType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_cdrs.md#43-cdrdimensiontype-enum
    """

    # defined in kWh, default step_size is 1 Wh
    energy = "ENERGY"
    # flat fee, no unit
    flat = "FLAT"
    # defined in A (Ampere), Maximum current reached during charging session
    max_current = "MAX_CURRENT"
    # defined in A (Ampere), Minimum current used during charging session
    min_current = "MIN_CURRENT"
    # time not charging: defined in hours, default step_size is 1 second
    parking_time = "PARKING_TIME"
    # time charging: defined in hours, default step_size is 1 second
    time = "TIME"
