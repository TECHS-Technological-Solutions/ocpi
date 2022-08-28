from enum import Enum


class RoleEnum(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/types.asciidoc#151-role-enum
    """
    cpo = 'Charge Point Operator Role.'
    emsp = 'eMobility Service Provider Role.'
    hub = 'Hub role.'
    nap = 'National Access Point Role (national Database with all Location information of a country).'
    nsp = 'Navigation Service Provider Role, role like an eMSP (probably only interested in Location information).'
    other = 'Other role.'
    scsp = 'Smart Charging Service Provider Role.'


class ModuleID(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#124-moduleid-enum
    """
    cdrs = 'cdrs'
    charging_profile = 'chargingprofiles'
    commands = 'commands'
    credentials_and_registration = 'credentials'
    hub_client_info = 'hubclientinfo'
    locations = 'locations'
    sessions = 'sessions'
    tariffs = 'tariffs'
    tokens = 'tokens'
