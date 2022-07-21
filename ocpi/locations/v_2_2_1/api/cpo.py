from typing import List

from fastapi import APIRouter
from ocpi.adapter.v_2_2_1 import Adapter

from ocpi.crud import CRUD
from ocpi.core.v_2_2_1.data_types import CiString
from ocpi.core.v_2_2_1.enums import ModuleID
from ocpi.locations.v_2_2_1.schemas import EVSE, Connector, Location

router = APIRouter(
    prefix='/locations',
)


@router.get("/", response_model=List[Location])
def get_locations():
    data_list = CRUD.list(ModuleID.Locations)
    locations = []
    for data in data_list:
        locations.append(Adapter.location_adapter(data))
    return locations


@router.get("/{location_id}", response_model=Location)
def get_location(location_id: CiString):
    data = CRUD.get(ModuleID.Locations, location_id)
    return Adapter.location_adapter(data)


@router.get("/{location_id}/{evse_uid}", response_model=EVSE)
def get_evse(location_id: CiString, evse_uid: CiString):
    data = CRUD.get(ModuleID.Locations, location_id)
    location = Adapter.location_adapter(data)
    for evse in location.evses:
        if evse.uid == evse_uid:
            return evse


@router.get("/{location_id}/{evse_uid}/{connector_id}", response_model=Connector)
def get_connector(location_id: CiString, evse_uid: CiString, connector_id: CiString):
    data = CRUD.get(ModuleID.Locations, location_id)
    location = Adapter.location_adapter(data)
    for evse in location.evses:
        if evse.uid == evse_uid:
            for connector in evse.connectors:
                if connector.id == connector_id:
                    return connector
