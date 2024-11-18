from enum import Enum


class ConnectionStatus(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_hub_client_info.asciidoc#151-connectionstatus-enum
    """
    connected = "CONNECTED"
    offline = "OFFLINE"
    planned = "PLANNED"
    suspended = "SUSPENDED"
