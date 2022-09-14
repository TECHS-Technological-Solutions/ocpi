from email.policy import default
from fastapi import APIRouter, Request, Depends, Query
from pydantic import ValidationError

from py_ocpi.core import status
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.utils import get_auth_token
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.tokens.v_2_2_1.enums import TokenType
from py_ocpi.tokens.v_2_2_1.schemas import Token, TokenUpdate

router = APIRouter(
    prefix='/tokens',
)


@router.get("/{country_code}/{party_id}/{token_uid}", response_model=OCPIResponse)
async def get_token(country_code: CiString(2), party_id: CiString(3), token_uid: CiString(36),
                    request: Request, token_type: TokenType = TokenType.rfid,
                    crud=Depends(get_crud), adapter=Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        data = await crud.get(ModuleID.tokens, token_uid,
                              auth_token=auth_token, country_code=country_code,
                              party_id=party_id, token_type=token_type)
        return OCPIResponse(
            data=[adapter.token_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.put("/{country_code}/{party_id}/{token_uid}", response_model=OCPIResponse)
async def add_token(country_code: CiString(2), party_id: CiString(3), token_uid: CiString(36), token: Token,
                    request: Request, token_type: TokenType = TokenType.rfid,
                    crud=Depends(get_crud), adapter=Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        data = await crud.create(ModuleID.tokens, token,
                                 auth_token=auth_token,
                                 country_code=country_code, party_id=party_id,
                                 token_uid=token_uid, token_type=token_type)
        return OCPIResponse(
            data=[adapter.token_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.patch("/{country_code}/{party_id}/{token_uid}", response_model=OCPIResponse)
async def update_token(country_code: CiString(2), party_id: CiString(3), token_uid: CiString(36), token: TokenUpdate,
                       request: Request, token_type: TokenType = TokenType.rfid,
                       crud=Depends(get_crud), adapter=Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        data = await crud.update(ModuleID.tokens, token, token_uid,
                                 auth_token=auth_token, country_code=country_code,
                                 party_id=party_id, token_type=token_type)
        return OCPIResponse(
            data=[adapter.token_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )
