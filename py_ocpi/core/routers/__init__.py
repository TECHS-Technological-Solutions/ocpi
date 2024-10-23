from py_ocpi.modules.versions.enums import VersionNumber

from .v_2_2_1 import ROUTERS_DICT as V_2_2_1_ROUTERS_DICT
from .v_2_1_1 import ROUTERS_DICT as V_2_1_1_ROUTERS_DICT


ROUTERS = {
    VersionNumber.v_2_2_1: V_2_2_1_ROUTERS_DICT,
    VersionNumber.v_2_1_1: V_2_1_1_ROUTERS_DICT,
}
