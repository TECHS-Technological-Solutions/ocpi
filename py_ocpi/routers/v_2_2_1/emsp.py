from fastapi import APIRouter

from py_ocpi.modules.credentials.v_2_2_1.api import emsp_router as credentials_emsp_2_2_1_router
from py_ocpi.modules.locations.v_2_2_1.api import emsp_router as locations_emsp_2_2_1_router


router = APIRouter(
)
router.include_router(
    locations_emsp_2_2_1_router
)
router.include_router(
    credentials_emsp_2_2_1_router
)
