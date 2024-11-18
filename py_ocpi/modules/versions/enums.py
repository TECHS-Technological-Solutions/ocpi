from enum import Enum


class VersionNumber(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#125-versionnumber-enum
    """
    v_2_0 = "2.0"
    v_2_1 = "2.1"
    v_2_1_1 = "2.1.1"
    v_2_2 = "2.2"
    v_2_2_1 = "2.2.1"
    latest = "2.2.1"
