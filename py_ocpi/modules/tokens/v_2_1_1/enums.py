from enum import Enum


class Allowed(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tokens.md#41-allowed-enum
    """

    # This Token is allowed to charge at this location.
    allowed = "ALLOWED"
    # This Token is blocked.
    blocked = "BLOCKED"
    # This Token has expired.
    expired = "EXPIRED"
    # This Token belongs to an account that has not enough credits to charge
    # at the given location.
    no_credit = "NO_CREDIT"
    # Token is valid, but is not allowed to charge at the given location.
    not_allowed = "NOT_ALLOWED"


class TokenType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tokens.md#43-tokentype-enum
    """

    # Other type of token
    other = "OTHER"
    # RFID Token
    rfid = "RFID"


class WhitelistType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tokens.md#44-whitelisttype-enum
    """

    # Token always has to be whitelisted, realtime authorization
    # is not possible/allowed.
    always = "ALWAYS"
    # It is allowed to whitelist the token, realtime authorization
    # is also allowed.
    allowed = "ALLOWED"
    # Whitelisting is only allowed when CPO cannot reach the eMSP
    # (communication between CPO and eMSP is offline)
    allowed_offline = "ALLOWED_OFFLINE"
    # Whitelisting is forbidden, only realtime authorization is allowed.
    # Token should always be authorized by the eMSP.
    never = "NEVER"
