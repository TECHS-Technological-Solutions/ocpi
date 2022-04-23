from enum import Enum


class RoleEnum(Enum, str):
    """
    https://github.com/ocpi/ocpi/blob/master/types.asciidoc#151-role-enum
    """
    CPO = 'Charge Point Operator Role.'
    EMSP = 'eMobility Service Provider Role.'
    HUB = 'Hub role.'
    NAP = 'National Access Point Role (national Database with all Location information of a country).'
    NSP = 'Navigation Service Provider Role, role like an eMSP (probably only interested in Location information).'
    OTHER = 'Other role.'
    SCSP = 'Smart Charging Service Provider Role.'


class ModuleID(Enum, str):
    """
    https://github.com/ocpi/ocpi/blob/master/version_information_endpoint.asciidoc#124-moduleid-enum
    """
    CDRs = 'cdrs'
    ChargingProfiles = 'chargingprofiles'
    Commands = 'commands'
    CredentialsAndRegistrations = 'credentials'
    HubClientInfo = 'hubclientinfo'
    Locations = 'locations'
    Sessions = 'sessions'
    Tariffs = 'tariffs'
    Tokens = 'tokens'
