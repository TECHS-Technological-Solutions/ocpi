from py_ocpi.modules.tariffs.enums import *  # noqa


class TariffDimensionType(str, Enum):  # noqa
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tariffs.md#44-tariffdimensiontype-enum
    """

    # defined in kWh, step_size multiplier: 1 Wh
    energy = "ENERGY"
    # flat fee, no unit
    flat = "FLAT"
    # time not charging: defined in hours, step_size multiplier: 1 second
    parking_time = "PARKING_TIME"
    # time charging: defined in hours, step_size multiplier: 1 second
    time = "TIME"
