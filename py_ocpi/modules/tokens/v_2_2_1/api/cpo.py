import copy

from fastapi import APIRouter, Request, Depends

from py_ocpi.core import status
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.config import logger
from py_ocpi.core.utils import get_auth_token, partially_update_attributes
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.tokens.v_2_2_1.enums import TokenType
from py_ocpi.modules.tokens.v_2_2_1.schemas import Token, TokenPartialUpdate

router = APIRouter(
    prefix="/tokens",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_2_1))],
)


@router.get(
    "/{country_code}/{party_id}/{token_uid}", response_model=OCPIResponse
)
async def get_token(
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    token_uid: CiString(36),  # type: ignore
    request: Request,
    token_type: TokenType = TokenType.rfid,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Get Token.

    Retrieves information about a token based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - token_uid (str): The ID of the token (36 characters).

    **Query parameters:**
        - token_type (TokenType): The type of the token (default=TokenType.rfid).

    **Returns:**
        The OCPIResponse containing the token information.

    **Raises:**
        NotFoundOCPIError: If the token is not found.
    """
    logger.info("Received request to get token with id - `%s`." % token_uid)
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.tokens,
        RoleEnum.cpo,
        token_uid,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        token_type=token_type,
        version=VersionNumber.v_2_2_1,
    )
    if data:
        return OCPIResponse(
            data=[adapter.token_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    logger.debug("Token with id `%s` was not found." % token_uid)
    raise NotFoundOCPIError


@router.put(
    "/{country_code}/{party_id}/{token_uid}", response_model=OCPIResponse
)
async def add_or_update_token(
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    token_uid: CiString(36),  # type: ignore
    token: Token,
    request: Request,
    token_type: TokenType = TokenType.rfid,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Add or Update Token.

    Adds or updates a token based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - token_uid (str): The ID of the token (36 characters).

    **Query parameters:**
        - token_type (TokenType): The type of the token (default=TokenType.rfid).

    **Request body:**
        token (Token): The token object.

    **Returns:**
        The OCPIResponse containing the token data.
    """
    logger.info(
        "Received request to add or update token with id - `%s`." % token_uid
    )
    logger.debug("Token data to update - %s" % token.dict())
    auth_token = get_auth_token(request)

    data = await crud.get(
        ModuleID.tokens,
        RoleEnum.cpo,
        token_uid,
        auth_token=auth_token,
        token_type=token_type,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if data:
        logger.debug("Update token with id - `%s`." % token_uid)
        data = await crud.update(
            ModuleID.tokens,
            RoleEnum.cpo,
            token.dict(),
            token_uid,
            token_type=token_type,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )
    else:
        logger.debug("Create token with id - `%s`." % token_uid)
        data = await crud.create(
            ModuleID.tokens,
            RoleEnum.cpo,
            token.dict(),
            token_type=token_type,
            auth_token=auth_token,
            country_code=country_code,
            party_id=party_id,
            version=VersionNumber.v_2_2_1,
        )
    return OCPIResponse(
        data=[adapter.token_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.patch(
    "/{country_code}/{party_id}/{token_uid}", response_model=OCPIResponse
)
async def partial_update_token(
    country_code: CiString(2),  # type: ignore
    party_id: CiString(3),  # type: ignore
    token_uid: CiString(36),  # type: ignore
    token: TokenPartialUpdate,
    request: Request,
    token_type: TokenType = TokenType.rfid,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Partial Update Token.

    Partially updates a token based on the specified parameters.

    **Path parameters:**
        - country_code (str): The two-letter country code.
        - party_id (str): The three-letter party ID.
        - token_uid (str): The ID of the token (36 characters).

    **Query parameters:**
        - token_type (TokenType): The type of the token (default=TokenType.rfid).

    **Request body:**
        token (TokenPartialUpdate): The partial token update object.

    **Returns:**
        The OCPIResponse containing the partially updated token data.

    **Raises:**
        NotFoundOCPIError: If the token is not found.
    """
    logger.info(
        "Received request to partially update token with id - `%s`." % token_uid
    )
    logger.debug("Token data to update - %s" % token.dict())
    auth_token = get_auth_token(request)

    old_data = await crud.get(
        ModuleID.tokens,
        RoleEnum.cpo,
        token_uid,
        token_type=token_type,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    if not old_data:
        logger.debug("Token with id `%s` was not found." % token_uid)

        raise NotFoundOCPIError
    old_token = adapter.token_adapter(old_data)

    new_token = copy.deepcopy(old_token)
    partially_update_attributes(
        new_token, token.dict(exclude_defaults=True, exclude_unset=True)
    )

    data = await crud.update(
        ModuleID.tokens,
        RoleEnum.cpo,
        new_token.dict(),
        token_uid,
        token_type=token_type,
        auth_token=auth_token,
        country_code=country_code,
        party_id=party_id,
        version=VersionNumber.v_2_2_1,
    )
    return OCPIResponse(
        data=[adapter.token_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
