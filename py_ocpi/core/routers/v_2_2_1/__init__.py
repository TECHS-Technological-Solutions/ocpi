from py_ocpi.routers import v_2_2_1_cpo_router, v_2_2_1_emsp_router
from py_ocpi.modules.versions import versions_v_2_2_1_router

ROUTERS_DICT = {
    "version_router": versions_v_2_2_1_router,
    "cpo_router": v_2_2_1_cpo_router,
    "emsp_router": v_2_2_1_emsp_router,
}
