from py_ocpi.core.enums import ModuleID
from py_ocpi.core.endpoints.v_2_2_1.utils import emsp_generator
from py_ocpi.modules.versions.v_2_2_1.schemas import InterfaceRole


CREDENTIALS_AND_REGISTRATION = emsp_generator.generate_endpoint(
    ModuleID.credentials_and_registration,
    InterfaceRole.receiver,
)

LOCATIONS = emsp_generator.generate_endpoint(
    ModuleID.locations,
    InterfaceRole.receiver,
)

SESSIONS = emsp_generator.generate_endpoint(
    ModuleID.sessions,
    InterfaceRole.receiver,
)

CDRS = emsp_generator.generate_endpoint(
    ModuleID.cdrs,
    InterfaceRole.receiver,
)

TARIFFS = emsp_generator.generate_endpoint(
    ModuleID.tariffs,
    InterfaceRole.receiver,
)

COMMANDS = emsp_generator.generate_endpoint(
    ModuleID.commands,
    InterfaceRole.sender,
)

TOKENS = emsp_generator.generate_endpoint(
    ModuleID.tokens,
    InterfaceRole.sender,
)

HUB_CLIENT_INFO = emsp_generator.generate_endpoint(
    ModuleID.hub_client_info,
    InterfaceRole.receiver,
)

CHARGING_PROFILE = emsp_generator.generate_endpoint(
    ModuleID.charging_profile,
    InterfaceRole.sender,
)

ENDPOINTS_LIST = {
    ModuleID.credentials_and_registration: CREDENTIALS_AND_REGISTRATION,
    ModuleID.locations: LOCATIONS,
    ModuleID.sessions: SESSIONS,
    ModuleID.cdrs: CDRS,
    ModuleID.tariffs: TARIFFS,
    ModuleID.commands: COMMANDS,
    ModuleID.tokens: TOKENS,
    ModuleID.hub_client_info: HUB_CLIENT_INFO,
    ModuleID.charging_profile: CHARGING_PROFILE,
}
