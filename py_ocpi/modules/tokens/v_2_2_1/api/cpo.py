from fastapi import APIRouter, Request, Depends
from pydantic import ValidationError

from py_ocpi.core import status
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core.utils import get_auth_token, partially_update_attributes
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.tokens.v_2_2_1.enums import TokenType
from py_ocpi.modules.tokens.v_2_2_1.schemas import Token, TokenPartialUpdate

router = APIRouter(
    prefix='/tokens',
)


@router.get("/{country_code}/{party_id}/{token_uid}", response_model=OCPIResponse)
async def get_token(country_code: CiString(2), party_id: CiString(3), token_uid: CiString(36),
                    request: Request, token_type: TokenType = TokenType.rfid,
                    crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    data = await crud.get(ModuleID.tokens, RoleEnum.cpo, token_uid,
                          auth_token=auth_token, country_code=country_code,
                          party_id=party_id, token_type=token_type,
                          version=VersionNumber.v_2_2_1)
    return OCPIResponse(
        data=[adapter.token_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.put("/{country_code}/{party_id}/{token_uid}", response_model=OCPIResponse)
async def add_or_update_token(country_code: CiString(2), party_id: CiString(3), token_uid: CiString(36), token: Token,
                              request: Request, token_type: TokenType = TokenType.rfid,
                              crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    data = await crud.get(ModuleID.tokens, RoleEnum.cpo, token_uid, auth_token=auth_token,
                          token_type=token_type, country_code=country_code, party_id=party_id,
                          version=VersionNumber.v_2_2_1)
    if data:
        data = await crud.update(ModuleID.tokens, RoleEnum.cpo, token.dict(), token_uid, token_type=token_type,
                                 auth_token=auth_token, country_code=country_code,
                                 party_id=party_id, version=VersionNumber.v_2_2_1)
    else:
        data = await crud.create(ModuleID.tokens, RoleEnum.cpo, token.dict(), token_type=token_type,
                                 auth_token=auth_token, country_code=country_code,
                                 party_id=party_id, version=VersionNumber.v_2_2_1)
    return OCPIResponse(
        data=[adapter.token_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.patch("/{country_code}/{party_id}/{token_uid}", response_model=OCPIResponse)
async def partial_update_token(country_code: CiString(2), party_id: CiString(3), token_uid: CiString(36),
                               token: TokenPartialUpdate, request: Request, token_type: TokenType = TokenType.rfid,
                               crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    old_data = await crud.get(ModuleID.tokens, RoleEnum.cpo, token_uid, token_type=token_type,
                              auth_token=auth_token, country_code=country_code, party_id=party_id,
                              version=VersionNumber.v_2_2_1)
    old_token = adapter.token_adapter(old_data)

    new_token = old_token
    partially_update_attributes(new_token, token.dict(exclude_defaults=True, exclude_unset=True))

    data = await crud.update(ModuleID.tokens, RoleEnum.cpo, new_token.dict(), token_uid, token_type=token_type,
                             auth_token=auth_token, country_code=country_code,
                             party_id=party_id, version=VersionNumber.v_2_2_1)
    return OCPIResponse(
        data=[adapter.token_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
