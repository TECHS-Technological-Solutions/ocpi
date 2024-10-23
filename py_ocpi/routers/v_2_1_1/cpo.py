from py_ocpi.core.enums import ModuleID

from py_ocpi.modules.credentials.v_2_1_1.api import (
    cpo_router as credentials_cpo_2_1_1_router,
)
from py_ocpi.modules.locations.v_2_1_1.api import (
    cpo_router as locations_cpo_2_1_1_router,
)
from py_ocpi.modules.cdrs.v_2_1_1.api import (
    cpo_router as cdrs_cpo_2_1_1_router,
)
from py_ocpi.modules.tariffs.v_2_1_1.api import (
    cpo_router as tariffs_cpo_2_1_1_router,
)
from py_ocpi.modules.sessions.v_2_1_1.api import (
    cpo_router as sessions_cpo_2_1_1_router,
)
from py_ocpi.modules.tokens.v_2_1_1.api import (
    cpo_router as tokens_cpo_2_1_1_router,
)
from py_ocpi.modules.commands.v_2_1_1.api import (
    cpo_router as commands_cpo_2_1_1_router,
)

router = {
    ModuleID.locations: locations_cpo_2_1_1_router,
    ModuleID.credentials_and_registration: credentials_cpo_2_1_1_router,
    ModuleID.cdrs: cdrs_cpo_2_1_1_router,
    ModuleID.tariffs: tariffs_cpo_2_1_1_router,
    ModuleID.sessions: sessions_cpo_2_1_1_router,
    ModuleID.tokens: tokens_cpo_2_1_1_router,
    ModuleID.commands: commands_cpo_2_1_1_router,
}
