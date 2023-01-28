from fastapi import APIRouter

from py_ocpi.modules.versions.schemas import VersionDetail
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.endpoints import ENDPOINTS
from py_ocpi.core.enums import RoleEnum

router = APIRouter()


@router.get("/", response_model=OCPIResponse)
async def get_version_details():
    return OCPIResponse(
        data=[
            VersionDetail(
                version=VersionNumber.v_2_2_1,
                endpoints=ENDPOINTS[VersionNumber.v_2_2_1][RoleEnum.cpo]
            ).dict(),
        ],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
