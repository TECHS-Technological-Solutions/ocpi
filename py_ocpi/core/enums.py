from enum import Enum


class RoleEnum(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/types.asciidoc#151-role-enum
    """

    # Charge Point Operator Role
    cpo = "CPO"
    # eMobility Service Provider Role
    emsp = "EMSP"
    # Hub role
    hub = "HUB"
    # National Access Point Role
    # (national Database with all Location information of a country)
    nap = "NAP"
    # Navigation Service Provider Role, role like an eMSP
    # (probably only interested in Location information)
    nsp = "NSP"
    # Other role
    other = "OTHER"
    # Smart Charging Service Provider Role
    scsp = "SCSP"


class ModuleID(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#124-moduleid-enum
    """

    cdrs = "cdrs"
    charging_profile = "chargingprofiles"
    commands = "commands"
    credentials_and_registration = "credentials"
    hub_client_info = "hubclientinfo"
    client_info = "clientinfo"
    locations = "locations"
    sessions = "sessions"
    tariffs = "tariffs"
    tokens = "tokens"


class Action(str, Enum):
    # used for requesting to send an OCPP command to a Chargepoint
    send_command = "SendCommand"
    # used for getting client authentication token
    get_client_token = "GetClientToken"  # nosec
    # used for authorizing a token
    authorize_token = "AuthorizeToken"  # nosec
    # used for requesting to send command to a Chargepoint
    send_get_chargingprofile = "SendGetChargingProfile"  # nosec
    # used for requesting to send command to a Chargepoint
    send_delete_chargingprofile = "SendDeleteChargingProfile"  # nosec
    # used for requesting to send command to a Chargepoint
    send_update_charging_profile = "SendUpdateChargingProfile"  # nosec


class EnvironmentType(str, Enum):
    production = "production"
    development = "development"
    testing = "testing"
