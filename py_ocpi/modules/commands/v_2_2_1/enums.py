from enum import Enum


class CommandResponseType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_commands.asciidoc#141-commandresponsetype-enum
    """
    # The requested command is not supported by this CPO, Charge Point, EVSE etc.
    not_supported = 'NOT_SUPPORTED'
    # Command request rejected by the CPO. (Session might not be from a customer of the eMSP that send this request)
    rejected = 'REJECTED'
    # Command request accepted by the CPO.
    accepted = 'ACCEPTED'
    # The Session in the requested command is not known by this CPO
    unknown_session = 'UNKNOWN_SESSION'


class CommandResultType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_commands.asciidoc#142-commandresulttype-enum
    """
    # Command request accepted by the Charge Point.
    accepted = 'ACCEPTED'
    # The Reservation has been canceled by the CPO.
    canceled_reservation = 'CANCELED_RESERVATION'
    # EVSE is currently occupied, another session is ongoing. Cannot start a new session
    evse_occupied = 'EVSE_OCCUPIED'
    # EVSE is currently inoperative or faulted.
    evse_inoperative = 'EVSE_INOPERATIVE'
    # Execution of the command failed at the Charge Point.
    failed = 'FAILED'
    # The requested command is not supported by this Charge Point, EVSE etc.
    not_supported = 'NOT_SUPPORTED'
    # Command request rejected by the Charge Point.
    rejected = 'REJECTED'
    # Command request timeout, no response received from the Charge Point in a reasonable time.
    timeout = 'TIMEOUT'
    # The Reservation in the requested command is not known by this Charge Point.
    unknown_reservation = 'UNKNOWN_RESERVATION'


class CommandType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_commands.asciidoc#143-commandtype-enum
    """
    # Request the Charge Point to cancel a specific reservation.
    cancel_reservation = 'CANCEL_RESERVATION'
    # Request the Charge Point to reserve a (specific) EVSE for a Token for a certain time, starting now.
    reserve_now = 'RESERVE_NOW'
    # Request the Charge Point to start a transaction on the given EVSE/Connector.
    start_session = 'START_SESSION'
    # Request the Charge Point to stop an ongoing session.
    stop_session = 'STOP_SESSION'
    # Request the Charge Point to unlock the connector (if applicable).
    # This functionality is for help desk operators only!
    unlock_connector = 'UNLOCK_CONNECTOR'
