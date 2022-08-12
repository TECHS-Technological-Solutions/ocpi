from enum import Enum


class ProfileType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_sessions.asciidoc#142-profiletype-enum
    """
    # Driver wants to use the cheapest charging profile possible.
    cheap = 'CHEAP'
    # Driver wants his EV charged as quickly as possible and is willing to pay a premium for this, if needed.
    fast = 'FAST'
    # Driver wants his EV charged with as much regenerative (green) energy as possible.
    green = 'GREEN'
    # Driver does not have special preferences.
    regular = 'REGULAR'
