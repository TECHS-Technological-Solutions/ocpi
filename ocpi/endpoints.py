from ocpi.core.v_2_2_1.enums import ModuleID
from ocpi.core.v_2_2_1.data_types import URL
from ocpi.core.config import settings
from ocpi.versions.schemas import Endpoint
from ocpi.versions.enums import VersionNumber, InterfaceRole

ENDPOINTS = {
    VersionNumber.v_2_2_1: [
        # locations
        Endpoint(
            identifier=ModuleID.Locations,
            role=InterfaceRole.Receiver,
            url=URL(f'https://{settings.HOST}/cpo/{VersionNumber.v_2_2_1}/{ModuleID.Locations}')
        ),
    ]

}
