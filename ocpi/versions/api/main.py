from fastapi import APIRouter

from ocpi.versions.schemas import Version, VersionDetail, URL
from ocpi.versions.enums import VersionNumber

from ocpi.core.v_2_2_1.schemas import OCPIResponse
from ocpi.core.config import settings
from ocpi.core.v_2_2_1 import status
from ocpi.endpoints import ENDPOINTS

router = APIRouter()


@router.get("/versions", response_model=OCPIResponse)
def get_versions():
    return OCPIResponse(
        data=Version(
            version=VersionNumber.v_2_2_1,
            url=URL(f'https://{settings.HOST}/cpo/2.2.1')
        ).dict(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.get("/2.2.1/details", response_model=OCPIResponse)
def get_version_details():
    return OCPIResponse(
        data=VersionDetail(
            version=VersionNumber.v_2_2_1,
            endpoints=ENDPOINTS[VersionNumber.v_2_2_1]
        ).dict(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
