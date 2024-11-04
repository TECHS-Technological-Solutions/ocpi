from fastapi import APIRouter, Depends, Request, Response

from py_ocpi.modules.cdrs.v_2_1_1.schemas import Cdr
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import get_auth_token
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.config import logger
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.config import settings
from py_ocpi.core.dependencies import get_crud, get_adapter

router = APIRouter(
    prefix="/cdrs",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_1_1))],
)


@router.get("/{cdr_id}", response_model=OCPIResponse)
async def get_cdr(
    request: Request,
    cdr_id: CiString(36),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get CDR by ID.

    Retrieves a Charge Detail Record (CDR) based on the specified ID.

    **Path parameters:**
        - cdr_id (str): The ID of the CDR to retrieve (36 characters).

    **Returns:**
        The OCPIResponse containing the CDR data.

    **Raises:**
        NotFoundOCPIError: If the CDR is not found.
    """
    logger.info(f"Received request to get cdr with id - `{cdr_id}`.")
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.get(
        ModuleID.cdrs,
        RoleEnum.emsp,
        cdr_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_1_1,
    )
    if data:
        return OCPIResponse(
            data=[adapter.cdr_adapter(data, VersionNumber.v_2_1_1).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug(f"CDR with id `{cdr_id}` was not found.")
    raise NotFoundOCPIError


@router.post("/", response_model=OCPIResponse)
async def add_cdr(
    request: Request,
    response: Response,
    cdr: Cdr,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Add CDR.

    Creates a new Charge Detail Record (CDR) based on the specified parameters.

    **Request body:**
        cdr (Cdr): The CDR object.

    **Returns:**
        The OCPIResponse containing the created CDR data.
    """
    logger.info("Received request to create cdr.")
    logger.debug(f"CDR data to create - {cdr.dict()}")
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.create(
        ModuleID.cdrs,
        RoleEnum.emsp,
        cdr.dict(),
        auth_token=auth_token,
        version=VersionNumber.v_2_1_1,
    )

    cdr_data = adapter.cdr_adapter(data, VersionNumber.v_2_1_1)
    cdr_url = (
        f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp"
        f"/{VersionNumber.v_2_1_1}/{ModuleID.cdrs}/{cdr_data.id}"
    )
    response.headers.append("Location", cdr_url)

    return OCPIResponse(
        data=[cdr_data.dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
