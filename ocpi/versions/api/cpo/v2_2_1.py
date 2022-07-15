from fastapi import APIRouter

from versions.schemas import Version, VersionDetail, URL
from versions.enums import VersionNumber
from ocpi.core.schemas import OCPIResponse
from ocpi.core.config import settings
from ocpi.endpoints import ENDPOINTS
from ocpi.core import status

router = APIRouter()


@router.get("/versions", response_model=OCPIResponse)
def get_versions():
    return OCPIResponse(
        data=Version(
            version=VersionNumber._2_2_1,
            url=URL(f'https://{settings.HOST}/cpo/2.2.1')
        ).dict(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.get("/2.2.1/details", response_model=OCPIResponse)
def get_version_details():
    return OCPIResponse(
        data=VersionDetail(
            version=VersionNumber._2_2_1,
            endpoints=ENDPOINTS
        ).dict(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
