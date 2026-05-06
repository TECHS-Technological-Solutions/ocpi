from typing import List
from pydantic import BaseModel, validator

from py_ocpi.core.data_types import CiString, URL, String
from py_ocpi.core.enums import RoleEnum
from py_ocpi.modules.locations.v_2_2_1.schemas import BusinessDetails


class CredentialsRole(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/credentials.asciidoc#141-credentialsrole-class
    """
    role: RoleEnum
    business_details: BusinessDetails
    party_id: CiString(3)
    country_code: CiString(2)

    @validator('country_code')
    def country_code_to_upper(cls, v):
        return v.upper()
    
    @validator('party_id')
    def party_id_to_upper(cls, v):
        return v.upper()

class Credentials(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/credentials.asciidoc#131-credentials-object
    """
    token: String(64)
    url: URL
    roles: List[CredentialsRole]
