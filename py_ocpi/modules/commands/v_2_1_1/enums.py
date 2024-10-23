from enum import Enum


class CommandResponseType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_commands.md#41-commandresponsetype-enum
    """

    # The requested command is not supported by this CPO,
    # Charge Point, EVSE etc.
    not_supported = "NOT_SUPPORTED"
    # Command request rejected by the CPO or Charge Point.
    rejected = "REJECTED"
    # Command request accepted by the CPO or Charge Point.
    accepted = "ACCEPTED"
    # Command request timeout, no response received from
    # the Charge Point in a reasonable time.
    timeout = "TIMEOUT"
    # The Session in the requested command is not known by this CPO.
    unknown_session = "UNKNOWN_SESSION"


class CommandType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_commands.md#42-commandtype-enum
    """

    # Request the Charge Point to reserve a (specific) EVSE
    # for a Token for a certain time, starting now.
    reserve_now = "RESERVE_NOW"
    # Request the Charge Point to start a transaction on
    # the given EVSE/Connector.
    start_session = "START_SESSION"
    # Request the Charge Point to stop an ongoing session.
    stop_session = "STOP_SESSION"
    # Request the Charge Point to unlock the connector (if applicable).
    # This functionality is for help desk operators only!
    unlock_connector = "UNLOCK_CONNECTOR"
