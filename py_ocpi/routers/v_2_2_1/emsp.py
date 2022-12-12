from fastapi import APIRouter

from py_ocpi.modules.credentials.v_2_2_1.api import emsp_router as credentials_emsp_2_2_1_router
from py_ocpi.modules.locations.v_2_2_1.api import emsp_router as locations_emsp_2_2_1_router
from py_ocpi.modules.sessions.v_2_2_1.api import emsp_router as sessions_emsp_2_2_1_router
from py_ocpi.modules.cdrs.v_2_2_1.api import emsp_router as cdrs_emsp_2_2_1_router
from py_ocpi.modules.tariffs.v_2_2_1.api import emsp_router as tariffs_emsp_2_2_1_router
from py_ocpi.modules.commands.v_2_2_1.api import emsp_router as commands_emsp_2_2_1_router


router = APIRouter(
)
router.include_router(
    locations_emsp_2_2_1_router
)
router.include_router(
    credentials_emsp_2_2_1_router
)
router.include_router(
    sessions_emsp_2_2_1_router
)
router.include_router(
    cdrs_emsp_2_2_1_router
)
router.include_router(
    tariffs_emsp_2_2_1_router
)
router.include_router(
    commands_emsp_2_2_1_router
)
