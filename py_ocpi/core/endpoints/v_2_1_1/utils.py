from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.endpoints.utils import BaseEndpointGenerator
from py_ocpi.core.data_types import URL
from py_ocpi.modules.versions.v_2_1_1.schemas import (
    Endpoint,
    VersionNumber,
)


class BaseEndpointGenerator211(BaseEndpointGenerator):
    """
    Endpoint generator which uses Endpoint schema v2.1.1

    :param role: The role type.
    """

    def __init__(self, role: RoleEnum) -> None:
        self.version = VersionNumber.v_2_1_1
        super().__init__(version=self.version, role=role)

    def generate_endpoint(
        self,
        module: ModuleID,
        *args,
        **kwargs,
    ) -> Endpoint:
        """
        Return generated Endpoint schema.

        :param module: Module type.
        """
        url = self.format_url(self.version, self.role, module)
        return Endpoint(identifier=module, url=URL(url))


class CPOEndpointGenerator211(BaseEndpointGenerator211):
    """Endpoint generator for CPO role using Endpoint schema v2.1.1."""

    def __init__(self):
        self.role = RoleEnum.cpo
        super().__init__(role=self.role)


class EMSPEndpointGenerator211(BaseEndpointGenerator211):
    """Endpoint generator for EMSP role using Endpoint schema v2.1.1."""

    def __init__(self):
        self.role = RoleEnum.emsp
        super().__init__(role=self.role)


cpo_generator = CPOEndpointGenerator211()
emsp_generator = EMSPEndpointGenerator211()
