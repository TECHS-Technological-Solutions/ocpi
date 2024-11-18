from py_ocpi.core.enums import ModuleID

from py_ocpi.modules.credentials.v_2_2_1.api import (
    emsp_router as credentials_emsp_2_2_1_router,
)
from py_ocpi.modules.locations.v_2_2_1.api import (
    emsp_router as locations_emsp_2_2_1_router,
)
from py_ocpi.modules.sessions.v_2_2_1.api import (
    emsp_router as sessions_emsp_2_2_1_router,
)
from py_ocpi.modules.cdrs.v_2_2_1.api import (
    emsp_router as cdrs_emsp_2_2_1_router,
)
from py_ocpi.modules.tariffs.v_2_2_1.api import (
    emsp_router as tariffs_emsp_2_2_1_router,
)
from py_ocpi.modules.commands.v_2_2_1.api import (
    emsp_router as commands_emsp_2_2_1_router,
)
from py_ocpi.modules.tokens.v_2_2_1.api import (
    emsp_router as tokens_emsp_2_2_1_router,
)
from py_ocpi.modules.hubclientinfo.v_2_2_1.api import (
    emsp_router as hubclientinfo_emsp_2_2_1_router,
)
from py_ocpi.modules.chargingprofiles.v_2_2_1.api import (
    emsp_router as chargingprofiles_emsp_2_2_1_router,
)


router = {
    ModuleID.locations: locations_emsp_2_2_1_router,
    ModuleID.credentials_and_registration: credentials_emsp_2_2_1_router,
    ModuleID.sessions: sessions_emsp_2_2_1_router,
    ModuleID.commands: commands_emsp_2_2_1_router,
    ModuleID.tariffs: tariffs_emsp_2_2_1_router,
    ModuleID.tokens: tokens_emsp_2_2_1_router,
    ModuleID.cdrs: cdrs_emsp_2_2_1_router,
    ModuleID.hub_client_info: hubclientinfo_emsp_2_2_1_router,
    ModuleID.charging_profile: chargingprofiles_emsp_2_2_1_router,
}
