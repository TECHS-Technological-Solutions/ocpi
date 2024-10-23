from pydantic import BaseModel

from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.core.data_types import URL


class Version(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#121-data
    """
    version: VersionNumber
    url: URL
