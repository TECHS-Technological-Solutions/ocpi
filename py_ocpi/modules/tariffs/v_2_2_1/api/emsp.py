from fastapi import APIRouter, Depends, Request

from py_ocpi.modules.tariffs.v_2_2_1.schemas import Tariff
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
from py_ocpi.core.dependencies import get_crud, get_adapter

router = APIRouter(
    prefix="/tariffs",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_2_1))],
)


@router.get(
    "/{country_code}/{party_id}/{tariff_id}", response_model=OCPIResponse
)
async def get_tariff(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    tariff_id: CiString(36),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get Tariff.

    Retrieves a tariff based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - tariff_id (str): The ID of the tariff (36 characters).

    **Returns:**
        The OCPIResponse containing the tariff data.

    **Raises:**
        NotFoundOCPIError: If the tariff is not found.
    """
    logger.info("Received request to get tariff with id - `%s`." % tariff_id)
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.tariffs,
        RoleEnum.emsp,
        tariff_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if data:
        return OCPIResponse(
            data=[adapter.tariff_adapter(data, VersionNumber.v_2_2_1).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Tariff with id `%s` was not found." % tariff_id)
    raise NotFoundOCPIError


@router.put(
    "/{country_code}/{party_id}/{tariff_id}", response_model=OCPIResponse
)
async def add_or_update_tariff(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    tariff_id: CiString(36),  # type: ignore
    tariff: Tariff,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Add or Update Tariff.

    Adds or updates a tariff based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - tariff_id (str): The ID of the tariff (36 characters).

    **Request body:**
        tariff (Tariff): The tariff object.

    **Returns:**
        The OCPIResponse containing the tariff data.
    """
    logger.info(
        "Received request to add or update tariff with id - `%s`." % tariff_id
    )
    logger.debug("Tariff data to update - %s" % tariff.dict())
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.tariffs,
        RoleEnum.emsp,
        tariff_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if data:
        logger.debug("Update tariff with id - `%s`." % tariff_id)
        data = await crud.update(
            ModuleID.tariffs,
            RoleEnum.emsp,
            tariff.dict(),
            tariff_id,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )
    else:
        logger.debug("Create tariff with id - `%s`." % tariff_id)
        data = await crud.create(
            ModuleID.tariffs,
            RoleEnum.emsp,
            tariff.dict(),
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )

    return OCPIResponse(
        data=[adapter.tariff_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.delete(
    "/{country_code}/{party_id}/{tariff_id}", response_model=OCPIResponse
)
async def delete_tariff(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    tariff_id: CiString(36),  # type: ignore
    crud: Crud = Depends(get_crud),
):
    """
    Delete Tariff.

    Deletes a tariff based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - tariff_id (str): The ID of the tariff to delete (36 characters).

    **Returns:**
        The OCPIResponse indicating the success of the operation.

    **Raises:**
        NotFoundOCPIError: If the tariff is not found.
    """
    logger.info("Received request to delete tariff with id - `%s`." % tariff_id)
    auth_token = get_auth_token(request)

    tariff = await crud.get(
        ModuleID.tariffs,
        RoleEnum.emsp,
        tariff_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if tariff:
        await crud.delete(
            ModuleID.tariffs,
            RoleEnum.emsp,
            tariff_id,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )

        return OCPIResponse(
            data=[],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Tariff with id `%s` was not found." % tariff_id)
    raise NotFoundOCPIError
