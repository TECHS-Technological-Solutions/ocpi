from fastapi import APIRouter, Depends

from py_ocpi.modules.versions.schemas import VersionDetail
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.dependencies import get_endpoints

router = APIRouter()


@router.get("/2.2.1/details", response_model=OCPIResponse)
async def get_version_details(endpoints=Depends(get_endpoints)):
    return OCPIResponse(
        data=VersionDetail(
            version=VersionNumber.v_2_2_1,
            endpoints=endpoints[VersionNumber.v_2_2_1]
        ).dict(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
