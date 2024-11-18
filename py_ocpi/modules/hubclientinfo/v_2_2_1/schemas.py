from pydantic import BaseModel

from py_ocpi.core.data_types import CiString, DateTime
from py_ocpi.core.enums import RoleEnum
from py_ocpi.modules.hubclientinfo.v_2_2_1.enums import ConnectionStatus


class ClientInfo(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.2.1-bugfixes/mod_hub_client_info.asciidoc#141-clientinfo-object
    """
    party_id: CiString(3)
    country_code: CiString(2)
    role: RoleEnum
    status: ConnectionStatus
    last_updated: DateTime
