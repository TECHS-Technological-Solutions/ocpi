import urllib

from fastapi import APIRouter, Depends, Response, Request
from pydantic import ValidationError

from py_ocpi.adapter import get_adapter
from py_ocpi.crud import get_crud
from py_ocpi.filters import pagination_filters
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.config import settings
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID
from py_ocpi.versions.enums import VersionNumber

router = APIRouter(
    prefix='/locations',
)


@router.get("/", response_model=OCPIResponse)
async def get_locations(response: Response,
                        crud=Depends(get_crud),
                        adapter=Depends(get_adapter),
                        filters: dict = Depends(pagination_filters)):
    try:
        data_list, total, is_last_page = await crud.list(ModuleID.Locations, filters)

        link = ''
        params = dict(**filters, offset=filters['offset'] + filters['limit'])
        if not is_last_page:
            link = (f'<https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                    f'/{VersionNumber.v_2_2_1}/{ModuleID.Locations}/?{urllib.parse.urlencode(params)}>; rel="next"')

        # set pagination headers
        response.headers['Link'] = link
        response.headers['X-Total-Count'] = total
        response.headers['X-Limit'] = filters['limit']

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
