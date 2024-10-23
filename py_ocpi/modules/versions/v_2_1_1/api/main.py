from fastapi import (
    APIRouter,
    Depends,
    Request,
    HTTPException,
    status as fastapistatus,
)

from py_ocpi.core.authentication.verifier import (
    VersionsAuthorizationVerifier,
)
from py_ocpi.core.crud import Crud
from py_ocpi.core import status
from py_ocpi.core.config import logger
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.dependencies import get_endpoints, get_crud

from py_ocpi.modules.versions.v_2_1_1.schemas import (
    VersionDetail,
    VersionNumber,
)

router = APIRouter()
cred_dependency = VersionsAuthorizationVerifier(VersionNumber.v_2_1_1)


@router.get("/2.1.1/details", response_model=OCPIResponse)
async def get_version_details(
    request: Request,
    endpoints=Depends(get_endpoints),
    crud: Crud = Depends(get_crud),
    server_cred: str | dict | None = Depends(cred_dependency),
):
    """
    Get Version Details.

    Retrieves details of the OCPI version 2.1.1.

    **Returns:**
        The OCPIResponse containing details of the OCPI version 2.1.1.
    """
    logger.info("Received request for version details: %s" % request.url)
    if server_cred is None:
        logger.debug("Unauthorized request.")
        raise HTTPException(fastapistatus.HTTP_401_UNAUTHORIZED, "Unauthorized")

    return OCPIResponse(
        data=VersionDetail(
            version=VersionNumber.v_2_1_1,
            endpoints=endpoints[VersionNumber.v_2_1_1],
        ).dict(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
