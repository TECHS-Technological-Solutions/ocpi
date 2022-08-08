from py_ocpi.core.enums import ModuleID
from py_ocpi.core.data_types import URL
from py_ocpi.core.config import settings
from py_ocpi.versions.schemas import Endpoint
from py_ocpi.versions.enums import VersionNumber, InterfaceRole

ENDPOINTS = {
    VersionNumber.v_2_2_1: [
        # locations
        Endpoint(
            identifier=ModuleID.Locations,
            role=InterfaceRole.Receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo/{VersionNumber.v_2_2_1}/{ModuleID.Locations}')
        ),
    ]

}
