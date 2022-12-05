from fastapi import APIRouter, Depends, Request
from pydantic import ValidationError

from py_ocpi.core.utils import get_auth_token, partially_update_attributes
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core.data_types import CiString
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.locations.v_2_2_1.schemas import (
    Location, LocationPartialUpdate,
    EVSE, EVSEPartialUpdate,
    Connector, ConnectorPartialUpdate,
)

router = APIRouter(
    prefix='/locations',
)


@router.get("/{country_code}/{party_id}/{location_id}", response_model=OCPIResponse)
async def get_location(request: Request, country_code: CiString(2), party_id: CiString(3), location_id: CiString(36),
                       crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        data = await crud.get(ModuleID.locations, RoleEnum.emsp, location_id, auth_token=auth_token,
                              country_code=country_code, party_id=party_id, version=VersionNumber.v_2_2_1)
        return OCPIResponse(
            data=[adapter.location_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.get("/{country_code}/{party_id}/{location_id}/{evse_uid}", response_model=OCPIResponse)
async def get_evse(request: Request, country_code: CiString(2), party_id: CiString(3), location_id: CiString(36),
                   evse_uid: CiString(48), crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        data = await crud.get(ModuleID.locations, RoleEnum.emsp, location_id, auth_token=auth_token,
                              country_code=country_code, party_id=party_id, version=VersionNumber.v_2_2_1)
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


@router.get("/{country_code}/{party_id}/{location_id}/{evse_uid}/{connector_id}", response_model=OCPIResponse)
async def get_connector(request: Request, country_code: CiString(2), party_id: CiString(3), location_id: CiString(36),
                        evse_uid: CiString(48), connector_id: CiString(36),
                        crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        data = await crud.get(ModuleID.locations, RoleEnum.emsp, location_id, auth_token=auth_token,
                              country_code=country_code, party_id=party_id, version=VersionNumber.v_2_2_1)
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


@router.put("/{country_code}/{party_id}/{location_id}", response_model=OCPIResponse)
async def add_or_update_location(request: Request, country_code: CiString(2), party_id: CiString(3),
                                 location_id: CiString(36), location: Location,
                                 crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        data = await crud.get(ModuleID.locations, RoleEnum.emsp, location_id, auth_token=auth_token,
                              country_code=country_code, party_id=party_id, version=VersionNumber.v_2_2_1)
        if data:
            data = await crud.update(ModuleID.locations, RoleEnum.emsp, location, location_id,
                                     auth_token=auth_token, country_code=country_code,
                                     party_id=party_id, version=VersionNumber.v_2_2_1)
        else:
            data = await crud.create(ModuleID.locations, RoleEnum.emsp, location,
                                     auth_token=auth_token, country_code=country_code,
                                     party_id=party_id, version=VersionNumber.v_2_2_1)

        return OCPIResponse(
            data=[adapter.location_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.put("/{country_code}/{party_id}/{location_id}/{evse_uid}", response_model=OCPIResponse)
async def add_or_update_evse(request: Request, country_code: CiString(2), party_id: CiString(3),
                             location_id: CiString(36), evse_uid: CiString(48), evse: EVSE,
                             crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        old_data = await crud.get(ModuleID.locations, RoleEnum.emsp, location_id, auth_token=auth_token,
                                  country_code=country_code, party_id=party_id, version=VersionNumber.v_2_2_1)
        old_location = adapter.location_adapter(old_data)

        is_new_evse = False
        for old_evse in old_location.evses:
            if old_evse.uid == evse_uid:
                is_new_evse = True
                break
        new_location = old_location
        if is_new_evse:
            new_location.evses.remove(old_evse)
        new_location.evses.append(evse)

        await crud.update(ModuleID.locations, RoleEnum.emsp, new_location, location_id,
                          auth_token=auth_token, country_code=country_code,
                          party_id=party_id, version=VersionNumber.v_2_2_1)

        return OCPIResponse(
            data=[evse.dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.put("/{country_code}/{party_id}/{location_id}/{evse_uid}/{connector_id}", response_model=OCPIResponse)
async def add_or_update_connector(request: Request, country_code: CiString(2), party_id: CiString(3),
                                  location_id: CiString(36), evse_uid: CiString(48),
                                  connector_id: CiString(36), connector: Connector,
                                  crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        old_data = await crud.get(ModuleID.locations, RoleEnum.emsp, location_id, auth_token=auth_token,
                                  country_code=country_code, party_id=party_id, version=VersionNumber.v_2_2_1)
        old_location = adapter.location_adapter(old_data)

        is_new_connector = False
        for old_evse in old_location.evses:
            if old_evse.uid == evse_uid:
                for old_onnector in old_evse.connectors:
                    if old_onnector.id == connector_id:
                        is_new_connector = True
                        break
        new_location = old_location
        if is_new_connector:
            new_location.evses.connectors.remove(old_onnector)
        new_location.evses.connectors.append(connector)

        await crud.update(ModuleID.locations, RoleEnum.emsp, new_location, location_id,
                          auth_token=auth_token, country_code=country_code,
                          party_id=party_id, version=VersionNumber.v_2_2_1)

        return OCPIResponse(
            data=[connector.dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.patch("/{country_code}/{party_id}/{location_id}", response_model=OCPIResponse)
async def partial_update_location(request: Request, country_code: CiString(2), party_id: CiString(3),
                                  location_id: CiString(36), location: LocationPartialUpdate,
                                  crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        old_data = await crud.get(ModuleID.locations, RoleEnum.emsp, location_id, auth_token=auth_token,
                                  country_code=country_code, party_id=party_id, version=VersionNumber.v_2_2_1)
        old_location = adapter.location_adapter(old_data)

        new_location = old_location
        partially_update_attributes(new_location, location.dict(exclude_defaults=True, exclude_unset=True))

        data = await crud.update(ModuleID.locations, RoleEnum.emsp, new_location, location_id,
                                 auth_token=auth_token, country_code=country_code,
                                 party_id=party_id, version=VersionNumber.v_2_2_1)

        return OCPIResponse(
            data=[adapter.location_adapter(data).dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.patch("/{country_code}/{party_id}/{location_id}/{evse_uid}", response_model=OCPIResponse)
async def partial_update_evse(request: Request, country_code: CiString(2), party_id: CiString(3),
                              location_id: CiString(36), evse_uid: CiString(48), evse: EVSEPartialUpdate,
                              crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        old_data = await crud.get(ModuleID.locations, RoleEnum.emsp, location_id, auth_token=auth_token,
                                  country_code=country_code, party_id=party_id, version=VersionNumber.v_2_2_1)
        old_location = adapter.location_adapter(old_data)

        for old_evse in old_location.evses:
            if old_evse.uid == evse_uid:
                break
        new_evse = old_evse
        partially_update_attributes(new_evse, evse.dict(exclude_defaults=True, exclude_unset=True))
        new_location = old_location

        await crud.update(ModuleID.locations, RoleEnum.emsp, new_location, location_id,
                          auth_token=auth_token, country_code=country_code,
                          party_id=party_id, version=VersionNumber.v_2_2_1)

        return OCPIResponse(
            data=[new_evse.dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.patch("/{country_code}/{party_id}/{location_id}/{evse_uid}/{connector_id}", response_model=OCPIResponse)
async def partial_update_connector(request: Request, country_code: CiString(2), party_id: CiString(3),
                                   location_id: CiString(36), evse_uid: CiString(48),
                                   connector_id: CiString(36), connector: ConnectorPartialUpdate,
                                   crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)
    try:
        old_data = await crud.get(ModuleID.locations, RoleEnum.emsp, location_id, auth_token=auth_token,
                                  country_code=country_code, party_id=party_id, version=VersionNumber.v_2_2_1)
        old_location = adapter.location_adapter(old_data)

        for old_evse in old_location.evses:
            if old_evse.uid == evse_uid:
                for old_onnector in old_evse.connectors:
                    if old_onnector.id == connector_id:
                        break
        new_connector = old_onnector
        partially_update_attributes(new_connector, connector.dict(exclude_defaults=True, exclude_unset=True))
        new_location = old_location

        await crud.update(ModuleID.locations, RoleEnum.emsp, new_location, location_id,
                          auth_token=auth_token, country_code=country_code,
                          party_id=party_id, version=VersionNumber.v_2_2_1)

        return OCPIResponse(
            data=[new_connector.dict()],
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )
