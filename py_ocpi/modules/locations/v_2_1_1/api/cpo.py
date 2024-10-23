from fastapi import APIRouter, Depends, Response, Request

from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import get_list, get_auth_token
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.config import logger
from py_ocpi.core.data_types import String
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.dependencies import get_crud, get_adapter, pagination_filters

router = APIRouter(
    prefix="/locations",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_1_1))],
)


@router.get("/", response_model=OCPIResponse)
async def get_locations(
    request: Request,
    response: Response,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    filters: dict = Depends(pagination_filters),
):
    """
    Get locations.

    Retrieves a list of locations based on the specified filters.

    **Query parameters:**
        - limit (int): Maximum number of objects to GET (default=50).
        - offset (int): The offset of the first object returned (default=0).
        - date_from (datetime): Only return Locations that have
            last_updated after this Date/Time (default=None).
        - date_to (datetime): Only return Locations that have
            last_updated before this Date/Time (default=None).

    **Returns:**
        The OCPIResponse containing the list of locations.
    """
    logger.info("Received request to get locations.")
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data_list = await get_list(
        response,
        filters,
        ModuleID.locations,
        RoleEnum.cpo,
        VersionNumber.v_2_1_1,
        crud,
        auth_token=auth_token,
    )

    locations = []
    for data in data_list:
        locations.append(
            adapter.location_adapter(data, VersionNumber.v_2_1_1).dict()
        )
    logger.debug(f"Amount of locations in response: {len(locations)}")
    return OCPIResponse(
        data=locations,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.get("/{location_id}", response_model=OCPIResponse)
async def get_location(
    request: Request,
    location_id: String(39),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get location by ID.

    Retrieves location details based on the specified ID.

    **Path parameters:**
        - location_id (str): The ID of the location to retrieve (39 characters).

    **Returns:**
        The OCPIResponse containing the location details.

    **Raises:**
        NotFoundOCPIError: If the location with the specified ID is not found.
    """
    logger.info("Received request to get location by id - `%s`." % location_id)
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.get(
        ModuleID.locations,
        RoleEnum.cpo,
        location_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_1_1,
    )
    if data:
        return OCPIResponse(
            data=[adapter.location_adapter(data, VersionNumber.v_2_1_1).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.get("/{location_id}/{evse_uid}", response_model=OCPIResponse)
async def get_evse(
    request: Request,
    location_id: String(39),  # type: ignore
    evse_uid: String(39),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get EVSE by ID.

    Retrieves Electric Vehicle Supply Equipment (EVSE) details
     based on the specified Location ID and EVSE UID.

    **Path parameters:**
        - location_id (str): The ID of the location containing
            the EVSE (39 characters).
        - evse_uid (str): The UID of the EVSE to retrieve (39 characters).

    **Returns:**
        The OCPIResponse containing the EVSE details.

    **Raises:**
        NotFoundOCPIError: If the location with the specified ID
            or EVSE with the specified UID is not found.
    """
    logger.info(
        "Received request to get evse by id - `%s` (location id - `%s`)"
        % (location_id, evse_uid)
    )
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.get(
        ModuleID.locations,
        RoleEnum.cpo,
        location_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_1_1,
    )
    if data:
        location = adapter.location_adapter(data, VersionNumber.v_2_1_1)
        for evse in location.evses:
            if evse.uid == evse_uid:
                return OCPIResponse(
                    data=[evse.dict()],
                    **status.OCPI_1000_GENERIC_SUCESS_CODE,
                )
        logger.debug("Evse with id `%s` was not found." % evse_uid)
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.get(
    "/{location_id}/{evse_uid}/{connector_id}", response_model=OCPIResponse
)
async def get_connector(
    request: Request,
    location_id: String(39),  # type: ignore
    evse_uid: String(39),  # type: ignore
    connector_id: String(36),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get Connector by ID.

    Retrieves Connector details based on the specified Location ID,
     EVSE UID, and Connector ID.

    **Path parameters:**
        - location_id (str): The ID of the location containing
            the EVSE (39 characters).
        - evse_uid (str): The UID of the EVSE to retrieve (39 characters).
        - connector_id (str): The ID of the connector
            to retrieve (36 characters).

    **Returns:**
        The OCPIResponse containing the Connector details.

    **Raises:**
        NotFoundOCPIError: If the location with the specified ID, EVSE with the
            specified UID, or Connector with the specified ID is not found.
    """
    logger.info(
        "Received request to get connector by id - `%s` "
        "(location id - `%s`, evse id - `%s`)"
        % (connector_id, location_id, evse_uid)
    )
    auth_token = get_auth_token(request, VersionNumber.v_2_1_1)

    data = await crud.get(
        ModuleID.locations,
        RoleEnum.cpo,
        location_id,
        auth_token=auth_token,
        version=VersionNumber.v_2_1_1,
    )
    if data:
        location = adapter.location_adapter(data, VersionNumber.v_2_1_1)
        for evse in location.evses:
            if evse.uid == evse_uid:
                for connector in evse.connectors:
                    if connector.id == connector_id:
                        return OCPIResponse(
                            data=[connector.dict()],
                            **status.OCPI_1000_GENERIC_SUCESS_CODE,
                        )
                logger.debug(
                    "Connector with id `%s` was not found." % connector_id
                )
        logger.debug("Evse with id `%s` was not found." % evse_uid)
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError
