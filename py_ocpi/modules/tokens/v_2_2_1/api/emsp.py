from fastapi import APIRouter, Depends, Response, Request

from py_ocpi.modules.tokens.v_2_2_1.enums import TokenType
from py_ocpi.modules.tokens.v_2_2_1.schemas import LocationReference
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import get_list, get_auth_token
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import AuthorizationVerifier
from py_ocpi.core.crud import Crud
from py_ocpi.core.config import logger
from py_ocpi.core.exceptions import NotFoundOCPIError
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID, RoleEnum, Action
from py_ocpi.core.dependencies import get_crud, get_adapter, pagination_filters

router = APIRouter(
    prefix="/tokens",
    dependencies=[Depends(AuthorizationVerifier(VersionNumber.v_2_2_1))],
)


@router.get("/", response_model=OCPIResponse)
async def get_tokens(
    request: Request,
    response: Response,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
    filters: dict = Depends(pagination_filters),
):
    """
    Get Tokens.

    Retrieves a list of tokens based on the specified filters.

    **Query parameters:**
        - limit (int): Maximum number of objects to GET (default=50).
        - offset (int): The offset of the first object returned (default=0).
        - date_from (datetime): Only return tokens that have last_updated
            after this Date/Time (default=None).
        - date_to (datetime): Only return tokens that have last_updated
            before this Date/Time (default=None).

    **Returns:**
        The OCPIResponse containing the list of tokens.
    """
    logger.info("Received request to get tokens")
    auth_token = get_auth_token(request)

    data_list = await get_list(
        response,
        filters,
        ModuleID.tokens,
        RoleEnum.emsp,
        VersionNumber.v_2_2_1,
        crud,
        auth_token=auth_token,
    )

    tokens = []
    for data in data_list:
        tokens.append(adapter.token_adapter(data).dict())
    logger.debug(f"Amount of tokens in response: {len(tokens)}")
    return OCPIResponse(
        data=tokens,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.post("/{token_uid}/authorize", response_model=OCPIResponse)
async def authorize_token(
    request: Request,
    response: Response,
    token_uid: CiString(36),  # type: ignore
    token_type: TokenType = TokenType.rfid,
    location_reference: LocationReference = None,  # type: ignore
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    """
    Authorize Token.

    Authorizes a token based on the specified parameters.

    **Path parameters:**
        - token_uid (str): The ID of the token to authorize (36 characters).

    **Query parameters:**
        - token_type (TokenType): The type of the token (default=TokenType.rfid).

    **Request body:**
        - location_reference (LocationReference): The location reference
            for authorization (default=None).

    **Returns:**
        The OCPIResponse containing the authorization result.

    **Raises:**
        NotFoundOCPIError: If the token is not found.
    """
    logger.info("Received request to authorize token with id `%s`" % token_uid)
    logger.debug("Token type - `%s`" % token_type)
    logger.debug("Location reference - `%s`" % location_reference)
    auth_token = get_auth_token(request)

    # check if token exists
    token = await crud.get(
        ModuleID.tokens,
        RoleEnum.emsp,
        token_uid,
        auth_token=auth_token,
        token_type=token_type,
        version=VersionNumber.v_2_2_1,
    )
    if token:
        location_reference = (
            location_reference.dict()
            if location_reference
            else None  # type: ignore
        )
        data = {
            "token_uid": token_uid,
            "token_type": token_type,
            "location_reference": location_reference,
        }
        authroization_result = await crud.do(
            ModuleID.tokens,
            RoleEnum.emsp,
            Action.authorize_token,
            data=data,
            auth_token=auth_token,
        )

        # when the token information is not enough
        if not authroization_result:
            logger.debug("Authorization result is null.")
            return OCPIResponse(
                data=[],
                **status.OCPI_2002_NOT_ENOUGH_INFORMATION,
            )

        return OCPIResponse(
            data=[adapter.authorization_adapter(authroization_result).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )

    logger.debug("Token with id `%s` was not found." % token_uid)
    raise NotFoundOCPIError
