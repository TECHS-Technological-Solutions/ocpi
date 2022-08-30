from fastapi import APIRouter, Depends, Response
from pydantic import ValidationError

from py_ocpi.versions.enums import VersionNumber
from py_ocpi.core.utils import get_list
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID
from py_ocpi.core.dependencies import get_crud, get_adapter, pagination_filters

router = APIRouter(
    prefix='/locations',
)


@router.get("/", response_model=OCPIResponse)
async def get_locations(response: Response,
                        crud=Depends(get_crud),
                        adapter=Depends(get_adapter),
                        filters: dict = Depends(pagination_filters)):
    try:
        data_list = await get_list(response, filters, ModuleID.locations,
                                   VersionNumber.v_2_2_1, crud)

        locations = []
        for data in data_list:
            locations.append(adapter.location_adapter(data).dict())
        return OCPIResponse(
            data=locations,
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.get("/{location_id}", response_model=OCPIResponse)
async def get_location(location_id: CiString(36), crud=Depends(get_crud), adapter=Depends(get_adapter)):
    try:
        data = await crud.get(ModuleID.locations, location_id)
        return OCPIResponse(
            data=[adapter.location_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.get("/{location_id}/{evse_uid}", response_model=OCPIResponse)
async def get_evse(location_id: CiString(36), evse_uid: CiString(48),
                   crud=Depends(get_crud), adapter=Depends(get_adapter)):
    try:
        data = await crud.get(ModuleID.locations, location_id)
        location = adapter.location_adapter(data)
        for evse in location.evses:
            if evse.uid == evse_uid:
                return OCPIResponse(
                    data=[evse.dict()],
                    **status.OCPI_1000_GENERIC_SUCESS_CODE,
                )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.get("/{location_id}/{evse_uid}/{connector_id}", response_model=OCPIResponse)
async def get_connector(location_id: CiString(36), evse_uid: CiString(48), connector_id: CiString(36),
                        crud=Depends(get_crud), adapter=Depends(get_adapter)):
    try:
        data = await crud.get(ModuleID.locations, location_id)
        location = adapter.location_adapter(data)
        for evse in location.evses:
            if evse.uid == evse_uid:
                for connector in evse.connectors:
                    if connector.id == connector_id:
                        return OCPIResponse(
                            data=[connector.dict()],
                            **status.OCPI_1000_GENERIC_SUCESS_CODE,
                        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )
