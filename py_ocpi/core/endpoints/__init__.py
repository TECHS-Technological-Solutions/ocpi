from py_ocpi.modules.versions.schemas import VersionNumber

from .v_2_2_1 import ENDPOINTS_DICT as V_2_2_1_ENDPOINTS_DICT
from .v_2_1_1 import ENDPOINTS_DICT as V_2_1_1_ENDPOINTS_DICT

ENDPOINTS: dict[str, dict] = {
    VersionNumber.v_2_2_1: V_2_2_1_ENDPOINTS_DICT,
    VersionNumber.v_2_1_1: V_2_1_1_ENDPOINTS_DICT,
}
