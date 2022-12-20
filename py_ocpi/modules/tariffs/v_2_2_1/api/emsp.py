from fastapi import APIRouter, Depends, Request

from py_ocpi.modules.tariffs.v_2_2_1.schemas import Tariff
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import get_auth_token
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.dependencies import get_crud, get_adapter

router = APIRouter(
    prefix='/tariffs',
)


@router.get("/{country_code}/{party_id}/{tariff_id}", response_model=OCPIResponse)
async def get_tariff(request: Request, country_code: CiString(2), party_id: CiString(3), tariff_id: CiString(36),
                     crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    data = await crud.get(ModuleID.tariffs, RoleEnum.emsp, tariff_id, auth_token=auth_token,
                          country_code=country_code, party_id=party_id, version=VersionNumber.v_2_2_1)
    return OCPIResponse(
        data=[adapter.tariff_adapter(data, VersionNumber.v_2_2_1).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.put("/{country_code}/{party_id}/{tariff_id}", response_model=OCPIResponse)
async def add_or_update_tariff(request: Request, country_code: CiString(2), party_id: CiString(3),
                               tariff_id: CiString(36), tariff: Tariff,
                               crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    data = await crud.get(ModuleID.tariffs, RoleEnum.emsp, tariff_id, auth_token=auth_token,
                          country_code=country_code, party_id=party_id, version=VersionNumber.v_2_2_1)
    if data:
        data = await crud.update(ModuleID.tariffs, RoleEnum.emsp, tariff.dict(), tariff_id,
                                 auth_token=auth_token, country_code=country_code,
                                 party_id=party_id, version=VersionNumber.v_2_2_1)
    else:
        data = await crud.create(ModuleID.tariffs, RoleEnum.emsp, tariff.dict(),
                                 auth_token=auth_token, country_code=country_code,
                                 party_id=party_id, version=VersionNumber.v_2_2_1)

    return OCPIResponse(
        data=[adapter.tariff_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.delete("/{country_code}/{party_id}/{tariff_id}", response_model=OCPIResponse)
async def delete_tariff(request: Request, country_code: CiString(2), party_id: CiString(3), tariff_id: CiString(36),
                        crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    await crud.delete(ModuleID.tariffs, RoleEnum.emsp, tariff_id,
                      auth_token=auth_token, country_code=country_code,
                      party_id=party_id, version=VersionNumber.v_2_2_1)

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
