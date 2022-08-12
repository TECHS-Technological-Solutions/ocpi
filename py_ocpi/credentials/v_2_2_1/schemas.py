from typing import List, Optional
from pydantic import BaseModel, validator

from py_ocpi.core.data_types import CiString, URL, String
from py_ocpi.core.enums import RoleEnum
from py_ocpi.locations.v_2_2_1.schemas import BusinessDetails, length_validator
from py_ocpi.versions.schemas import Version
from py_ocpi.endpoints import ENDPOINTS


class CredentialsRole(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/credentials.asciidoc#141-credentialsrole-class
    """
    role: RoleEnum
    business_details: BusinessDetails
    party_id: CiString
    country_code: CiString

    @validator('party_id')
    def validate_party_id(cls, v):
        length_validator('party_id', v, 3)
        return v

    @validator('country_code')
    def validate_country_code(cls, v):
        length_validator('country_code', v, 2)
        return v


class Credentials(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/credentials.asciidoc#131-credentials-object
    """
    token: String
    url: URL
    roles: List[CredentialsRole]

    @validator('token')
    def validate_latitude(cls, v):
        length_validator('token', v, 64)
        return v


class ServerCredentials(BaseModel):
    # Client's B token
    cred_token_b: String
    # Client's versions
    versions: Version
    # Client's endpoints
    endpoints: ENDPOINTS
    # Server versions URL
    url: Optional[URL]
    # Server business details
    roles: Optional[List[CredentialsRole]]

    @validator('cred_token_b')
    def validate_latitude(cls, v):
        length_validator('cred_token_b', v, 64)
        return v
