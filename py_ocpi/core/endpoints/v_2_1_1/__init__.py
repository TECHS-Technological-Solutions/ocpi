from py_ocpi.core.enums import RoleEnum

from .cpo import ENDPOINTS_LIST as CPO_ENDPOINTS_LIST
from .emsp import ENDPOINTS_LIST as EMSP_ENDPOINTS_LIST

ENDPOINTS_DICT = {
    RoleEnum.cpo: CPO_ENDPOINTS_LIST,
    RoleEnum.emsp: EMSP_ENDPOINTS_LIST,
}
