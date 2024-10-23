from abc import abstractmethod

from py_ocpi.core.config import settings
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.modules.versions.schemas import VersionNumber


class URLBuilder:
    """Base endpoint generator"""

    def __init__(self):
        self.protocol = settings.PROTOCOL
        self.ocpi_host = settings.OCPI_HOST
        self.ocpi_prefix = settings.OCPI_PREFIX
        self.trailing_slash = "/" if settings.TRAILING_SLASH else ""

    def format_url(
        self,
        version: VersionNumber,
        role: RoleEnum,
        module: ModuleID,
    ) -> str:
        """
        Return formatted url for endpoint.

        :param version: OCPI version.
        :param role: Role type.
        :param module: Module type.
        """
        if module == ModuleID.hub_client_info:
            module = ModuleID.client_info
        return (
            f"{self.protocol}://{self.ocpi_host}/{self.ocpi_prefix}/"
            f"{role.value.lower()}/{version.value}/{module.value}"
            f"{self.trailing_slash}"
        )


class BaseEndpointGenerator(URLBuilder):
    """
    Base endpoint generator providing common
    functionality for endpoint generation.

    :param version: The OCPI version.
    :param role: The role type.
    """

    def __init__(self, version: VersionNumber, role: RoleEnum) -> None:
        super().__init__()
        self.version = version
        self.role = role

    @abstractmethod
    def generate_endpoint(self, *args, **kwargs):
        """Abstract method for generating specific endpoints."""
        pass
