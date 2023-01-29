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
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.locations.value}')
        ),
        # sessions
        Endpoint(
            identifier=ModuleID.sessions,
            role=InterfaceRole.sender,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.sessions.value}')
        ),
        # credentials
        Endpoint(
            identifier=ModuleID.credentials_and_registration,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.credentials_and_registration.value}')
        ),
        # tariffs
        Endpoint(
            identifier=ModuleID.tariffs,
            role=InterfaceRole.sender,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.tariffs.value}')
        ),
        # cdrs
        Endpoint(
            identifier=ModuleID.cdrs,
            role=InterfaceRole.sender,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.cdrs.value}')
        ),
        # tokens
        Endpoint(
            identifier=ModuleID.tokens,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.tokens.value}')
        ),

        # ###############--EMSP--###############

        # credentials
        Endpoint(
            identifier=ModuleID.credentials_and_registration,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp'
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.credentials_and_registration.value}')
        ),
        # locations
        Endpoint(
            identifier=ModuleID.locations,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp'
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.locations.value}')
        ),
        # sessions
        Endpoint(
            identifier=ModuleID.sessions,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp'
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.sessions.value}')
        ),
        # cdrs
        Endpoint(
            identifier=ModuleID.cdrs,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp'
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.cdrs.value}')
        ),
        # tariffs
        Endpoint(
            identifier=ModuleID.tariffs,
            role=InterfaceRole.receiver,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp'
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.tariffs.value}')
        ),
        # commands
        Endpoint(
            identifier=ModuleID.commands,
            role=InterfaceRole.sender,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp'
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.commands.value}')
        ),
        # tokens
        Endpoint(
            identifier=ModuleID.tokens,
            role=InterfaceRole.sender,
            url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp'
                    f'/{VersionNumber.v_2_2_1.value}/{ModuleID.tokens.value}')
        ),
    ]

}
