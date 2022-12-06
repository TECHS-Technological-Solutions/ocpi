from py_ocpi.core.enums import ModuleID
from py_ocpi.core.data_types import URL
from py_ocpi.core.config import settings
from py_ocpi.modules.versions.schemas import Endpoint
from py_ocpi.modules.versions.enums import VersionNumber, InterfaceRole

ENDPOINTS = {
    VersionNumber.v_2_2_1: [
        # ###############--CPO--###############

        # locations
        Endpoint(
            identifier=ModuleID.locations,
            role=InterfaceRole.sender,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                    f'/{VersionNumber.v_2_2_1}/{ModuleID.locations}')
        ),
        # sessions
        Endpoint(
            identifier=ModuleID.sessions,
            role=InterfaceRole.sender,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                    f'/{VersionNumber.v_2_2_1}/{ModuleID.sessions}')
        ),
        # credentials
        Endpoint(
            identifier=ModuleID.credentials_and_registration,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                    f'/{VersionNumber.v_2_2_1}/{ModuleID.credentials_and_registration}')
        ),
        # tariffs
        Endpoint(
            identifier=ModuleID.tariffs,
            role=InterfaceRole.sender,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                    f'/{VersionNumber.v_2_2_1}/{ModuleID.tariffs}')
        ),
        # cdrs
        Endpoint(
            identifier=ModuleID.cdrs,
            role=InterfaceRole.sender,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                    f'/{VersionNumber.v_2_2_1}/{ModuleID.cdrs}')
        ),
        # tokens
        Endpoint(
            identifier=ModuleID.tokens,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                    f'/{VersionNumber.v_2_2_1}/{ModuleID.tokens}')
        ),

        # ###############--EMSP--###############

        # credentials
        Endpoint(
            identifier=ModuleID.credentials_and_registration,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp'
                    f'/{VersionNumber.v_2_2_1}/{ModuleID.credentials_and_registration}')
        ),
        # locations
        Endpoint(
            identifier=ModuleID.locations,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp'
                    f'/{VersionNumber.v_2_2_1}/{ModuleID.locations}')
        ),
        # sessions
        Endpoint(
            identifier=ModuleID.sessions,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp'
                    f'/{VersionNumber.v_2_2_1}/{ModuleID.sessions}')
        ),
        # cdrs
        Endpoint(
            identifier=ModuleID.cdrs,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp'
                    f'/{VersionNumber.v_2_2_1}/{ModuleID.cdrs}')
        ),
    ]

}
