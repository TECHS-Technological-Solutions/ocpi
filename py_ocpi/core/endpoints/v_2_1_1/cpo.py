from py_ocpi.core.enums import ModuleID
from py_ocpi.core.endpoints.v_2_1_1.utils import cpo_generator


CREDENTIALS_AND_REGISTRATION = cpo_generator.generate_endpoint(
    ModuleID.credentials_and_registration,
)

LOCATIONS = cpo_generator.generate_endpoint(ModuleID.locations)

CDRS = cpo_generator.generate_endpoint(ModuleID.cdrs)

TARIFFS = cpo_generator.generate_endpoint(ModuleID.tariffs)

SESSIONS = cpo_generator.generate_endpoint(ModuleID.sessions)

TOKENS = cpo_generator.generate_endpoint(ModuleID.tokens)

ENDPOINTS_LIST = {
    ModuleID.credentials_and_registration: CREDENTIALS_AND_REGISTRATION,
    ModuleID.locations: LOCATIONS,
    ModuleID.cdrs: CDRS,
    ModuleID.tariffs: TARIFFS,
    ModuleID.sessions: SESSIONS,
    ModuleID.tokens: TOKENS,
}
