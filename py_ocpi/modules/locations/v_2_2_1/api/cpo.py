from fastapi import APIRouter, Depends, Response, Request

from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.utils import get_list, get_auth_token
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.dependencies import get_crud, get_adapter, pagination_filters

router = APIRouter(
    prefix='/locations',
)


@router.get("/", response_model=OCPIResponse)
async def get_locations(request: Request,
                        response: Response,
                        crud: Crud = Depends(get_crud),
                        adapter: Adapter = Depends(get_adapter),
                        filters: dict = Depends(pagination_filters)):
    auth_token = get_auth_token(request)

    data_list = await get_list(response,  filters, ModuleID.locations, RoleEnum.cpo,
                               VersionNumber.v_2_2_1, crud, auth_token=auth_token)

    locations = []
    for data in data_list:
        locations.append(adapter.location_adapter(data).dict())
    return OCPIResponse(
        data=locations,
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.get("/{location_id}", response_model=OCPIResponse)
async def get_location(request: Request, location_id: CiString(36),
                       crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    data = await crud.get(ModuleID.locations, RoleEnum.cpo, location_id, auth_token=auth_token,
                          version=VersionNumber.v_2_2_1)
    return OCPIResponse(
        data=[adapter.location_adapter(data).dict()],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.get("/{location_id}/{evse_uid}", response_model=OCPIResponse)
async def get_evse(request: Request, location_id: CiString(36), evse_uid: CiString(48),
                   crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    data = await crud.get(ModuleID.locations, RoleEnum.cpo, location_id, auth_token=auth_token,
                          version=VersionNumber.v_2_2_1)
    location = adapter.location_adapter(data)
    for evse in location.evses:
        if evse.uid == evse_uid:
            return OCPIResponse(
                data=[evse.dict()],
                **status.OCPI_1000_GENERIC_SUCESS_CODE,
            )


@router.get("/{location_id}/{evse_uid}/{connector_id}", response_model=OCPIResponse)
async def get_connector(request: Request, location_id: CiString(36), evse_uid: CiString(48), connector_id: CiString(36),
                        crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    data = await crud.get(ModuleID.locations, RoleEnum.cpo, location_id, auth_token=auth_token,
                          version=VersionNumber.v_2_2_1)
    location = adapter.location_adapter(data)
    for evse in location.evses:
        if evse.uid == evse_uid:
            for connector in evse.connectors:
                if connector.id == connector_id:
                    return OCPIResponse(
                        data=[connector.dict()],
                        **status.OCPI_1000_GENERIC_SUCESS_CODE,
                    )
