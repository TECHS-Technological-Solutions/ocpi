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
from py_ocpi.core import status
from py_ocpi.core.config import logger
from py_ocpi.core.crud import Crud
from py_ocpi.core.dependencies import (
    get_versions as get_versions_,
    get_crud,
)
from py_ocpi.core.schemas import OCPIResponse


router = APIRouter()
cred_dependency = VersionsAuthorizationVerifier(None)


@router.get("/versions", response_model=OCPIResponse)
async def get_versions(
    request: Request,
    versions=Depends(get_versions_),
    crud: Crud = Depends(get_crud),
    server_cred: str | dict | None = Depends(cred_dependency),
):
    """
    Get OCPI Versions.

    Retrieves a list of available OCPI versions.

    **Returns:**
        The OCPIResponse containing a list of available OCPI versions.
    """
    logger.info("Received request for version details: %s" % request.url)
    if server_cred is None:
        logger.debug("Unauthorized request.")
        raise HTTPException(
            fastapistatus.HTTP_401_UNAUTHORIZED,
            "Unauthorized",
        )
    return OCPIResponse(
        data=versions,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
