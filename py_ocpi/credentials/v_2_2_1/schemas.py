from typing import List, Optional
from pydantic import BaseModel

from py_ocpi.core.data_types import CiString, URL, String
from py_ocpi.core.enums import RoleEnum
from py_ocpi.locations.v_2_2_1.schemas import BusinessDetails
from py_ocpi.versions.schemas import Version, Endpoint


class CredentialsRole(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/credentials.asciidoc#141-credentialsrole-class
    """
    role: RoleEnum
    business_details: BusinessDetails
    party_id: CiString(3)
    country_code: CiString(2)


class Credentials(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/credentials.asciidoc#131-credentials-object
    """
    token: String(64)
    url: URL
    roles: List[CredentialsRole]


class ServerCredentials(BaseModel):
    # Client's B token
    cred_token_b: String(max_length=64)
    # Client's versions
    versions: Version
    # Client's endpoints
    endpoints: Endpoint
    # Server versions URL
    url: Optional[URL]
    # Server business details
    roles: Optional[List[CredentialsRole]]
