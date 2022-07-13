from fastapi import APIRouter

from versions.schemas import Version, URL
from versions.enums import VersionNumber
from ocpi.core.schemas import OCPIResponse
from ocpi.core.config import settings
from ocpi.core import status

router = APIRouter(
    prefix='/versions',
)


@router.get("/", response_model=OCPIResponse)
def get_versions():
    return OCPIResponse(
        data=Version(
            version=VersionNumber._2_2_1,
            url=URL(f'{settings.HOST}/cpo/2.2.1')
        ).dict(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
