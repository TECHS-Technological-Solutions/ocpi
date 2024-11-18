from typing import List

from pydantic import BaseModel

from py_ocpi.modules.versions.v_2_1_1.enums import VersionNumber
from py_ocpi.core.data_types import URL
from py_ocpi.core.enums import ModuleID


class Endpoint(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/version_information_endpoint.md#endpoint-class
    """

    identifier: ModuleID
    url: URL


class VersionDetail(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/version_information_endpoint.md#data-1
    """

    version: VersionNumber
    endpoints: List[Endpoint]
