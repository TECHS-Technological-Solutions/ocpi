from py_ocpi.core.enums import ModuleID
from py_ocpi.core.endpoints.v_2_2_1.utils import cpo_generator
from py_ocpi.modules.versions.v_2_2_1.schemas import InterfaceRole


CREDENTIALS_AND_REGISTRATION = cpo_generator.generate_endpoint(
    ModuleID.credentials_and_registration,
    InterfaceRole.receiver,
)

LOCATIONS = cpo_generator.generate_endpoint(
    ModuleID.locations,
    InterfaceRole.sender,
)

SESSIONS = cpo_generator.generate_endpoint(
    ModuleID.sessions,
    InterfaceRole.sender,
)

CDRS = cpo_generator.generate_endpoint(
    ModuleID.cdrs,
    InterfaceRole.sender,
)

TARIFFS = cpo_generator.generate_endpoint(
    ModuleID.tariffs,
    InterfaceRole.sender,
)

TOKENS = cpo_generator.generate_endpoint(
    ModuleID.tokens,
    InterfaceRole.receiver,
)

HUB_CLIENT_INFO = cpo_generator.generate_endpoint(
    ModuleID.hub_client_info,
    InterfaceRole.receiver,
)

CHARGING_PROFILE = cpo_generator.generate_endpoint(
    ModuleID.charging_profile,
    InterfaceRole.receiver,
)


ENDPOINTS_LIST = {
    ModuleID.credentials_and_registration: CREDENTIALS_AND_REGISTRATION,
    ModuleID.locations: LOCATIONS,
    ModuleID.sessions: SESSIONS,
    ModuleID.cdrs: CDRS,
    ModuleID.tariffs: TARIFFS,
    ModuleID.tokens: TOKENS,
    ModuleID.hub_client_info: HUB_CLIENT_INFO,
    ModuleID.charging_profile: CHARGING_PROFILE,
}
