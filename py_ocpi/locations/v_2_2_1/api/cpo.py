from fastapi import APIRouter, Depends
from pydantic import ValidationError

from py_ocpi.adapter import get_adapter
from py_ocpi.crud import get_crud
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID

router = APIRouter(
    prefix='/locations',
)


@router.get("/", response_model=OCPIResponse)
async def get_locations(crud=Depends(get_crud), adapter=Depends(get_adapter)):
    try:
        data_list = await crud.list(ModuleID.Locations)
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
async def get_location(location_id: CiString, crud=Depends(get_crud), adapter=Depends(get_adapter)):
    try:
        data = await crud.get(ModuleID.Locations, location_id)
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
async def get_evse(location_id: CiString, evse_uid: CiString, crud=Depends(get_crud), adapter=Depends(get_adapter)):
    try:
        data = await crud.get(ModuleID.Locations, location_id)
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
async def get_connector(location_id: CiString, evse_uid: CiString, connector_id: CiString,
                        crud=Depends(get_crud), adapter=Depends(get_adapter)):
    try:
        data = await crud.get(ModuleID.Locations, location_id)
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
