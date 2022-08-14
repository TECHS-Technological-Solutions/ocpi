from enum import Enum


class ChargingPreferencesResponse(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_sessions.asciidoc#141-chargingpreferencesresponse-enum
    """
    # Charging Preferences accepted, EVSE will try to accomplish them,
    # although this is no guarantee that they will be fulfilled.
    accepted = 'ACCEPTED'
    # CPO requires departure_time to be able to perform Charging Preference based Smart Charging.
    departure_required = 'DEPARTURE_REQUIRED'
    # CPO requires energy_need to be able to perform Charging Preference based Smart Charging.
    energy_need_required = 'ENERGY_NEED_REQUIRED'
    # Charging Preferences contain a demand that the EVSE knows it cannot fulfill.
    not_possible = 'NOT_POSSIBLE'
    # profile_type contains a value that is not supported by the EVSE.
    profile_type_not_supported = 'PROFILE_TYPE_NOT_SUPPORTED'


class ProfileType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_sessions.asciidoc#142-profiletype-enum
    """
    # Driver wants to use the cheapest charging profile possible.
    cheap = 'CHEAP'
    # Driver wants his EV charged as quickly as possible and is willing to pay a premium for this, if needed.
    fast = 'FAST'
    # Driver wants his EV charged with as much regenerative (green) energy as possible.
    green = 'GREEN'
    # Driver does not have special preferences.
    regular = 'REGULAR'


class SessionStatus(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_sessions.asciidoc#143-sessionstatus-enum
    """
    # The session has been accepted and is active. All pre-conditions were met: Communication between EV and EVSE
    # (for example: cable plugged in correctly), EV or driver is authorized. EV is being charged, or can be charged.
    # Energy is, or is not, being transfered.
    active = 'ACTIVE'
    # The session has been finished successfully.
    # No more modifications will be made to the Session object using this state.
    completed = 'COMPLETED'
    # The Session object using this state is declared invalid and will not be billed.
    invalid = 'INVALID'
    # The session is pending, it has not yet started. Not all pre-conditions are met.
    # This is the initial state. The session might never become an active session.
    pending = 'PENDING'
    # The session is started due to a reservation, charging has not yet started.
    # The session might never become an active session.
    reservation = 'RESERVATION'
