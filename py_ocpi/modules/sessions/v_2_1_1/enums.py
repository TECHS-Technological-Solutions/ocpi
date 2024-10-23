from enum import Enum


class SessionStatus(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_sessions.md#41-sessionstatus-enum
    """

    # The session is accepted and active.
    # Al pre-condition are met: Communication between EV and EVSE
    # (for example: cable plugged in correctly), EV or Driver is authorized.
    # EV is being charged, or can be charged.
    # Energy is, or is not, being transferred.
    active = "ACTIVE"
    # The session is finished successfully.
    # No more modifications will be made to this session.
    completed = "COMPLETED"
    # The session is declared invalid and will not be billed.
    invalid = "INVALID"
    # The session is pending, it has not yet started.
    # Not all pre-condition are met.
    # This is the initial state.
    # This session might never become an active session.
    pending = "PENDING"
