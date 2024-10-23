import copy

from fastapi import APIRouter, Depends, Request

from py_ocpi.core.utils import get_auth_token, partially_update_attributes
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
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.locations.v_2_2_1.schemas import (
    Location,
    LocationPartialUpdate,
    EVSE,
    EVSEPartialUpdate,
    Connector,
    ConnectorPartialUpdate,
)

router = APIRouter(
    prefix="/locations",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_2_1))],
)


@router.get(
    "/{country_code}/{party_id}/{location_id}", response_model=OCPIResponse
)
async def get_location(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    location_id: CiString(36),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get Location.

    Retrieves a location based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str: The three-letter party ID.
        - location_id (str): The ID of the location to retrieve (36 characters).

    **Returns:**
        The OCPIResponse containing the location data.

    **Raises:**
        NotFoundOCPIError: NotFoundOCPIError: If the location is not found.
    """
    logger.info(
        "Received request to get location with id - `%s`." % location_id
    )
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if data:
        return OCPIResponse(
            data=[adapter.location_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.get(
    "/{country_code}/{party_id}/{location_id}/{evse_uid}",
    response_model=OCPIResponse,
)
async def get_evse(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    location_id: CiString(36),  # type: ignore
    evse_uid: CiString(48),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get EVSE.

    Retrieves an EVSE based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - location_id (str): The ID of the location containing
            the EVSE (36 characters).
        - evse_uid (str): The UID of the EVSE to retrieve (48 characters).

    **Returns:**
        The OCPIResponse containing the EVSE data.

    **Raises:**
        NotFoundOCPIError: If the location with the specified ID
         or EVSE with the specified UID is not found.
    """
    logger.info(
        "Received request to get evse by id - `%s` (location id - `%s`)"
        % (location_id, evse_uid)
    )
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if data:
        location = adapter.location_adapter(data)
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
    "/{country_code}/{party_id}/{location_id}/{evse_uid}/{connector_id}",
    response_model=OCPIResponse,
)
async def get_connector(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    location_id: CiString(36),  # type: ignore
    evse_uid: CiString(48),  # type: ignore
    connector_id: CiString(36),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get Connector.

    Retrieves a connector based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - location_id (str): The ID of the location containing
            the EVSE (36 characters).
        - evse_uid (str): The UID of the EVSE containing
            the connector (48 characters).
        - connector_id (str): The ID of the connector
            to retrieve (36 characters).

    **Returns:**
        The OCPIResponse containing the connector data.

    **Raises:**
        NotFoundOCPIError: If the location with the specified ID, EVSE with the
         specified UID, or Connector with the specified ID is not found.
    """
    logger.info(
        "Received request to get connector by id - `%s` "
        "(location id - `%s`, evse id - `%s`)"
        % (connector_id, location_id, evse_uid)
    )
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if data:
        location = adapter.location_adapter(data)
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


@router.put(
    "/{country_code}/{party_id}/{location_id}", response_model=OCPIResponse
)
async def add_or_update_location(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    location_id: CiString(36),  # type: ignore
    location: Location,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Add or Update Location.

    Adds or updates a location based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - location_id (str): The ID of the location to add
            or update (36 characters).

    **Request body:**
        location (Location): The location object.

    **Returns:**
        The OCPIResponse containing the added or updated location data.

    **Raises:**
        NotFoundOCPIError: If the location is not found.
    """
    logger.info(
        "Received request to add or update location with id - `%s`."
        % location_id
    )
    logger.debug("Location data to update - %s" % location.dict())
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if data:
        logger.debug("Update location with id - `%s`." % location_id)
        data = await crud.update(
            ModuleID.locations,
            RoleEnum.emsp,
            location.dict(),
            location_id,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )
    else:
        logger.debug("Create location with id - `%s`." % location_id)
        data = await crud.create(
            ModuleID.locations,
            RoleEnum.emsp,
            location.dict(),
            auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )

    return OCPIResponse(
        data=[adapter.location_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.put(
    "/{country_code}/{party_id}/{location_id}/{evse_uid}",
    response_model=OCPIResponse,
)
async def add_or_update_evse(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    location_id: CiString(36),  # type: ignore
    evse_uid: CiString(48),  # type: ignore
    evse: EVSE,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Add or Update EVSE.

    Adds or updates an EVSE based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - location_id (str): The ID of the location (36 characters).
        - evse_uid (str): The ID of the EVSE to add or update (48 characters).

    **Request body:**
        evse (EVSE): The EVSE object.

    **Returns:**
        The OCPIResponse containing the added or updated EVSE data.

    **Raises:**
        NotFoundOCPIError: If the location with the specified ID is not found.
    """
    logger.info(
        "Received request to add or update evse by id - `%s` "
        "(location id - `%s`)" % (location_id, evse_uid)
    )
    logger.debug("Evse data to update - %s" % evse.dict())
    auth_token = get_auth_token(request)

    old_data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if old_data:
        old_location = adapter.location_adapter(old_data)
        new_location = copy.deepcopy(old_location)

        for old_evse in old_location.evses:
            if old_evse.uid == evse_uid:
                logger.debug("Update evse with id - %s" % evse_uid)
                new_location.evses.remove(old_evse)
                break

        new_location.evses.append(evse)

        await crud.update(
            ModuleID.locations,
            RoleEnum.emsp,
            new_location.dict(),
            location_id,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )

        return OCPIResponse(
            data=[evse.dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.put(
    "/{country_code}/{party_id}/{location_id}/{evse_uid}/{connector_id}",
    response_model=OCPIResponse,
)
async def add_or_update_connector(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    location_id: CiString(36),  # type: ignore
    evse_uid: CiString(48),  # type: ignore
    connector_id: CiString(36),  # type: ignore
    connector: Connector,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Add or Update Connector.

    Adds or updates a connector based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - location_id (str): The ID of the location (36 characters).
        - evse_uid (str): The ID of the EVSE (48 characters).
        - connector_id (str): The ID of the connector to add
            or update (36 characters).

    **Request body:**
        connector (Connector): The connector object.

    **Returns:**
        The OCPIResponse containing the added or updated connector data.

    **Raises:**
        NotFoundOCPIError: If the location with the specified ID
            or EVSE with the specified UID is not found.
    """
    logger.info(
        "Received request to add or update connector by id - `%s` "
        "(location id - `%s`, evse id - `%s`)"
        % (connector_id, location_id, evse_uid)
    )
    logger.debug("Connector data to update - %s" % connector.dict())
    auth_token = get_auth_token(request)

    old_data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if old_data:
        old_location = adapter.location_adapter(old_data)
        new_location = copy.deepcopy(old_location)

        for old_evse in old_location.evses:
            if old_evse.uid == evse_uid:
                new_location.evses.remove(old_evse)
                new_evse = copy.deepcopy(old_evse)
                for old_connector in old_evse.connectors:
                    if old_connector.id == connector_id:
                        logger.debug(
                            "Update connector with id - %s" % connector_id
                        )
                        new_evse.connectors.remove(old_connector)
                        break
                new_evse.connectors.append(connector)
                new_location.evses.append(new_evse)

                await crud.update(
                    ModuleID.locations,
                    RoleEnum.emsp,
                    new_location.dict(),
                    location_id,
                    auth_token=auth_token,
                    country_code=country_code,
                    party_id=party_id,
                    version=VersionNumber.v_2_2_1,
                )

                return OCPIResponse(
                    data=[connector.dict()],
                    **status.OCPI_1000_GENERIC_SUCESS_CODE,
                )
        logger.debug("Evse with id `%s` was not found." % evse_uid)
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.patch(
    "/{country_code}/{party_id}/{location_id}", response_model=OCPIResponse
)
async def partial_update_location(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    location_id: CiString(36),  # type: ignore
    location: LocationPartialUpdate,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Partial Update Location.

    Partially updates a location based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - location_id (str): The ID of the location to partially
            update (36 characters).

    **Request body:**
        location (LocationPartialUpdate): The partial location update object.

    **Returns:**
        The OCPIResponse containing the partially updated location data.

    **Raises:**
        NotFoundOCPIError: If the location is not found.
    """
    logger.info(
        "Received request to partially update location with id - `%s`."
        % location_id
    )
    logger.debug("Location data to update - %s" % location.dict())
    auth_token = get_auth_token(request)

    old_data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if old_data:
        old_location = adapter.location_adapter(old_data)
        new_location = copy.deepcopy(old_location)

        partially_update_attributes(
            new_location,
            location.dict(exclude_defaults=True, exclude_unset=True),
        )

        data = await crud.update(
            ModuleID.locations,
            RoleEnum.emsp,
            new_location.dict(),
            location_id,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )

        return OCPIResponse(
            data=[adapter.location_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.patch(
    "/{country_code}/{party_id}/{location_id}/{evse_uid}",
    response_model=OCPIResponse,
)
async def partial_update_evse(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    location_id: CiString(36),  # type: ignore
    evse_uid: CiString(48),  # type: ignore
    evse: EVSEPartialUpdate,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Partial Update EVSE.

    Partially updates an EVSE based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - location_id (str): The ID of the location to partially
            update (36 characters).
        - evse_uid (str): The UID of the EVSE
            to partially update (48 characters).

    **Request body:**
        evse (EVSEPartialUpdate): The partial EVSE update object.

    **Returns:**
        The OCPIResponse containing the partially updated EVSE data.

    **Raises:**
        NotFoundOCPIError: If the location with the specified ID
         or EVSE with the specified UID is not found.
    """
    logger.info(
        "Received request to partially update evse by id - `%s` "
        "(location id - `%s`)" % (location_id, evse_uid)
    )
    logger.debug("Evse data to update - %s" % evse.dict())
    auth_token = get_auth_token(request)

    old_data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if old_data:
        old_location = adapter.location_adapter(old_data)
        new_location = copy.deepcopy(old_location)

        for old_evse in old_location.evses:
            if old_evse.uid == evse_uid:
                new_location.evses.remove(old_evse)
                new_evse = copy.deepcopy(old_evse)
                partially_update_attributes(
                    new_evse,
                    evse.dict(exclude_defaults=True, exclude_unset=True),
                )
                new_location.evses.append(new_evse)

                await crud.update(
                    ModuleID.locations,
                    RoleEnum.emsp,
                    new_location.dict(),
                    location_id,
                    auth_token=auth_token,
                    country_code=country_code,
                    party_id=party_id,
                    version=VersionNumber.v_2_2_1,
                )
                return OCPIResponse(
                    data=[new_evse.dict()],
                    **status.OCPI_1000_GENERIC_SUCESS_CODE,
                )
        logger.debug("Evse with id `%s` was not found." % evse_uid)
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError


@router.patch(
    "/{country_code}/{party_id}/{location_id}/{evse_uid}/{connector_id}",
    response_model=OCPIResponse,
)
async def partial_update_connector(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    location_id: CiString(36),  # type: ignore
    evse_uid: CiString(48),  # type: ignore
    connector_id: CiString(36),  # type: ignore
    connector: ConnectorPartialUpdate,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Partial Update Connector.

    Partially updates a connector based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - location_id (str): The ID of the location
            to partially update (36 characters).
        - evse_uid (str): The UID of the EVSE
            to partially update (48 characters).
        - connector_id (str): The ID of the connector
            to partially update (36 characters).

    **Request body:**
        connector (ConnectorPartialUpdate): The partial connector update object.

    **Returns:**
        The OCPIResponse containing the partially updated connector data.

    **Raises:**
        NotFoundOCPIError:If the location with the specified ID, EVSE with
         the specified UID, or Connector with the specified ID is not found.
    """
    logger.info(
        "Received request to partially update connector by id - `%s` "
        "(location id - `%s`, evse id - `%s`)"
        % (connector_id, location_id, evse_uid)
    )
    logger.debug("Connector data to update - %s" % connector.dict())
    auth_token = get_auth_token(request)

    old_data = await crud.get(
        ModuleID.locations,
        RoleEnum.emsp,
        location_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if old_data:
        old_location = adapter.location_adapter(old_data)

        for old_evse in old_location.evses:
            if old_evse.uid == evse_uid:
                for old_connector in old_evse.connectors:
                    if old_connector.id == connector_id:
                        new_connector = old_connector
                        partially_update_attributes(
                            new_connector,
                            connector.dict(
                                exclude_defaults=True, exclude_unset=True
                            ),
                        )
                        new_location = old_location

                        await crud.update(
                            ModuleID.locations,
                            RoleEnum.emsp,
                            new_location.dict(),
                            location_id,
                            auth_token=auth_token,
                            country_code=country_code,
                            party_id=party_id,
                            version=VersionNumber.v_2_2_1,
                        )

                        return OCPIResponse(
                            data=[new_connector.dict()],
                            **status.OCPI_1000_GENERIC_SUCESS_CODE,
                        )
                logger.debug(
                    "Connector with id `%s` was not found." % connector_id
                )
        logger.debug("Evse with id `%s` was not found." % evse_uid)
    logger.debug("Location with id `%s` was not found." % location_id)
    raise NotFoundOCPIError
