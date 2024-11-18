from py_ocpi.core.enums import ModuleID
from py_ocpi.core.endpoints.v_2_1_1.utils import emsp_generator


CREDENTIALS_AND_REGISTRATION = emsp_generator.generate_endpoint(
    ModuleID.credentials_and_registration,
)

LOCATIONS = emsp_generator.generate_endpoint(ModuleID.locations)

CDRS = emsp_generator.generate_endpoint(ModuleID.cdrs)

TARIFFS = emsp_generator.generate_endpoint(ModuleID.tariffs)

SESSIONS = emsp_generator.generate_endpoint(ModuleID.sessions)

TOKENS = emsp_generator.generate_endpoint(ModuleID.tokens)

COMMANDS = emsp_generator.generate_endpoint(ModuleID.commands)

ENDPOINTS_LIST = {
    ModuleID.credentials_and_registration: CREDENTIALS_AND_REGISTRATION,
    ModuleID.locations: LOCATIONS,
    ModuleID.cdrs: CDRS,
    ModuleID.tariffs: TARIFFS,
    ModuleID.sessions: SESSIONS,
    ModuleID.tokens: TOKENS,
    ModuleID.commands: COMMANDS,
}
