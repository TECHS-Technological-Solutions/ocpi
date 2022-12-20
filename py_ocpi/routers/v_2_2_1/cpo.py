from fastapi import APIRouter

from py_ocpi.modules.credentials.v_2_2_1.api import cpo_router as credentials_cpo_2_2_1_router
from py_ocpi.modules.locations.v_2_2_1.api import cpo_router as locations_cpo_2_2_1_router
from py_ocpi.modules.sessions.v_2_2_1.api import cpo_router as sessions_cpo_2_2_1_router
from py_ocpi.modules.commands.v_2_2_1.api import cpo_router as commands_cpo_2_2_1_router
from py_ocpi.modules.tariffs.v_2_2_1.api import cpo_router as tariffs_cpo_2_2_1_router
from py_ocpi.modules.tokens.v_2_2_1.api import cpo_router as tokens_cpo_2_2_1_router
from py_ocpi.modules.cdrs.v_2_2_1.api import cpo_router as cdrs_cpo_2_2_1_router


router = APIRouter(
)
router.include_router(
    locations_cpo_2_2_1_router
)
router.include_router(
    credentials_cpo_2_2_1_router
)
router.include_router(
    sessions_cpo_2_2_1_router
)
router.include_router(
    commands_cpo_2_2_1_router
)
router.include_router(
    tariffs_cpo_2_2_1_router
)
router.include_router(
    tokens_cpo_2_2_1_router
)
router.include_router(
    cdrs_cpo_2_2_1_router
)
