from enum import Enum


class AuthMethod(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#141-authmethod-enum
    """
    # Authentication request has been sent to the eMSP.
    auth_request = 'AUTH_REQUEST'
    # Command like StartSession or ReserveNow used to start the Session,
    # the Token provided in the Command was used as authorization.
    command = 'COMMAND'
    # Whitelist used for authentication, no request to the eMSP has been performed.
    whitelist = 'WHITELIST'


class CdrDimensionType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#143-cdrdimensiontype-enum
    """
    # Average charging current during this ChargingPeriod: defined in A (Ampere).
    # When negative, the current is flowing from the EV to the grid.
    current = 'CURRENT'
    # Total amount of energy (dis-)charged during this ChargingPeriod: defined in kWh.
    # When negative, more energy was feed into the grid then charged into the EV.
    # Default step_size is 1.
    energy = 'ENERGY'
    # Total amount of energy feed back into the grid: defined in kWh.
    energy_export = 'ENERGY_EXPORT'
    # Total amount of energy charged, defined in kWh.
    energy_import = 'ENERGY_IMPORT'
    # Sum of the maximum current over all phases, reached during this ChargingPeriod: defined in A (Ampere).
    max_current = 'MAX_CURRENT'
    # Sum of the minimum current over all phases, reached during this ChargingPeriod, when negative,
    # current has flowed from the EV to the grid. Defined in A (Ampere).
    min_current = 'MIN_CURRENT'
    # Maximum power reached during this ChargingPeriod: defined in kW (Kilowatt).
    max_power = 'MAX_POWER'
    # Minimum power reached during this ChargingPeriod: defined in kW (Kilowatt),
    # when negative, the power has flowed from the EV to the grid.
    min_power = 'MIN_POWER'
    # Time during this ChargingPeriod not charging: defined in hours, default step_size multiplier is 1 second.
    parking_time = 'PARKING_TIME'
    # Average power during this ChargingPeriod: defined in kW (Kilowatt).
    # When negative, the power is flowing from the EV to the grid.
    power = 'POWER'
    # Time during this ChargingPeriod Charge Point has been reserved and not yet been in use for this customer:
    # defined in hours, default step_size multiplier is 1 second.
    reservation_time = 'RESERVATION_TIME'
    # Current state of charge of the EV, in percentage, values allowed: 0 to 100. See note below.
    state_of_change = 'STATE_OF_CHARGE'
    # Time charging during this ChargingPeriod: defined in hours, default step_size multiplier is 1 second.
    time = 'TIME'
