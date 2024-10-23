from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.endpoints.utils import BaseEndpointGenerator
from py_ocpi.core.data_types import URL
from py_ocpi.modules.versions.v_2_2_1.schemas import (
    Endpoint,
    InterfaceRole,
    VersionNumber,
)


class BaseEndpointGenerator221(BaseEndpointGenerator):
    def __init__(self, role: RoleEnum) -> None:
        self.version = VersionNumber.v_2_2_1
        super().__init__(version=self.version, role=role)

    def generate_endpoint(
        self,
        module: ModuleID,
        interface_role: InterfaceRole,
        *args,
        **kwargs,
    ) -> Endpoint:
        """
        Return generated Endpoint schema.

        :param module: Module type.
        :param interface_role: Interface role of endpoint.
        """
        url = self.format_url(self.version, self.role, module)
        return Endpoint(
            identifier=module,
            role=interface_role,
            url=URL(url),
        )


class CPOEndpointGenerator221(BaseEndpointGenerator221):
    """Endpoint generator for CPO role using Endpoint schema v2.2.1."""

    def __init__(self):
        self.role = RoleEnum.cpo
        super().__init__(role=self.role)


class EMSPEndpointGenerator221(BaseEndpointGenerator221):
    """Endpoint generator for EMSP role using Endpoint schema v2.2.1."""

    def __init__(self):
        self.role = RoleEnum.emsp
        super().__init__(role=self.role)


cpo_generator = CPOEndpointGenerator221()
emsp_generator = EMSPEndpointGenerator221()
