from pydantic import BaseModel

from ocpi.core.data_types import URL
from ocpi.core.enums import ModuleID

from .enums import VersionNumber, InterfaceRole


class Version(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/version_information_endpoint.asciidoc#121-data
    """
    version: VersionNumber
    url: URL


class Endpoint(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/version_information_endpoint.asciidoc#122-endpoint-class
    """
    identifier: ModuleID
    role: InterfaceRole
    url: URL
