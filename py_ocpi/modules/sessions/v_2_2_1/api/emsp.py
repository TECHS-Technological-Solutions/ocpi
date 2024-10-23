import copy

from fastapi import APIRouter, Depends, Request

from py_ocpi.modules.sessions.v_2_2_1.schemas import (
    SessionPartialUpdate,
    Session,
)
from py_ocpi.modules.versions.enums import VersionNumber
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

router = APIRouter(
    prefix="/sessions",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_2_1))],
)


@router.get(
    "/{country_code}/{party_id}/{session_id}", response_model=OCPIResponse
)
async def get_session(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    session_id: CiString(36),  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get Session.

    Retrieves a session based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - session_id (str): The ID of the session (36 characters).

    **Returns:**
        The OCPIResponse containing the session data.

    **Raises:**
        NotFoundOCPIError: If the session is not found.
    """
    logger.info("Received request to get session with id - `%s`." % session_id)
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.sessions,
        RoleEnum.emsp,
        session_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if data:
        return OCPIResponse(
            data=[adapter.session_adapter(data, VersionNumber.v_2_2_1).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Session with id `%s` was not found." % session_id)
    raise NotFoundOCPIError


@router.put(
    "/{country_code}/{party_id}/{session_id}", response_model=OCPIResponse
)
async def add_or_update_session(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    session_id: CiString(36),  # type: ignore
    session: Session,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Add or Update Session.

    Adds or updates a session based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - session_id (str): The ID of the session (36 characters).

    **Request body:**
        session (Session): The session object.

    **Returns:**
        The OCPIResponse containing the added or updated session data.
    """
    logger.info(
        "Received request to add or update session with id - `%s`." % session_id
    )
    logger.debug("Session data to update - %s" % session.dict())
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.sessions,
        RoleEnum.emsp,
        session_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if data:
        logger.debug("Update session with id - `%s`." % session_id)
        data = await crud.update(
            ModuleID.sessions,
            RoleEnum.emsp,
            session.dict(),
            session_id,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )
    else:
        logger.debug("Create session with id - `%s`." % session_id)
        data = await crud.create(
            ModuleID.sessions,
            RoleEnum.emsp,
            session.dict(),
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )

    return OCPIResponse(
        data=[adapter.session_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.patch(
    "/{country_code}/{party_id}/{session_id}", response_model=OCPIResponse
)
async def partial_update_session(
    request: Request,
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    session_id: CiString(36),  # type: ignore
    session: SessionPartialUpdate,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Partial Update Session.

    Partially updates a session based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - session_id (str): The ID of the session (36 characters).

    **Request body:**
        session (SessionPartialUpdate): The partial session update object.

    **Returns:**
        The OCPIResponse containing the partially updated session data.

    **Raises:**
        NotFoundOCPIError: If the session is not found.
    """
    logger.info(
        "Received request to partially update session with id - `%s`."
        % session_id
    )
    logger.debug("Session data to update - %s" % session.dict())
    auth_token = get_auth_token(request)

    old_data = await crud.get(
        ModuleID.sessions,
        RoleEnum.emsp,
        session_id,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if old_data:
        old_session = adapter.session_adapter(old_data)

        new_session = copy.deepcopy(old_session)
        partially_update_attributes(
            new_session, session.dict(exclude_defaults=True, exclude_unset=True)
        )

        data = await crud.update(
            ModuleID.sessions,
            RoleEnum.emsp,
            new_session.dict(),
            session_id,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )

        return OCPIResponse(
            data=[adapter.session_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Session with id `%s` was not found." % session_id)
    raise NotFoundOCPIError
