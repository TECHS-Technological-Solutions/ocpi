from typing import Optional, List
from pydantic import BaseModel, validator

from py_ocpi.core.data_types import String, CiString, DisplayText, DateTime
from py_ocpi.locations.v_2_2_1.schemas import length_validator
from py_ocpi.tokens.v_2_2_1.enums import AllowedType, TokenType, WhitelistType
from py_ocpi.sessions.v_2_2_1.enums import ProfileType


class EnergyContract(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_tokens.asciidoc#142-energycontract-class
    """
    supplier_name: String
    contract_id: Optional[String]

    @validator('supplier_name')
    def validate_supplier_name(cls, v):
        length_validator('supplier_name', v, 64)
        return v

    @validator('contract_id')
    def validate_contract_id(cls, v):
        length_validator('contract_id', v, 64)
        return v


class LocationReference(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_tokens.asciidoc#143-locationreferences-class
    """
    location_id: CiString
    evse_uids: List[CiString] = []

    @validator('location_id')
    def validate_location_id(cls, v):
        length_validator('location_id', v, 36)
        return v

    @validator('evse_uids')
    def validate_evse_uids(cls, v):
        for uid in v:
            length_validator('evse_uids', uid, 36)
        return v


class Token(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_tokens.asciidoc#132-token-object
    """
    country_code: CiString
    party_id: CiString
    uid: CiString
    type: TokenType
    contract_id: CiString
    visual_number: Optional[String]
    issuer: String
    group_id: Optional[CiString]
    valid: bool
    whitelist: WhitelistType
    language: Optional[String]
    default_profile_type: Optional[ProfileType]
    energy_contract: Optional[EnergyContract]
    last_updated: DateTime

    @validator('country_code')
    def validate_country_code(cls, v):
        length_validator('country_code', v, 2)
        return v

    @validator('party_id')
    def validate_party_id(cls, v):
        length_validator('party_id', v, 3)
        return v

    @validator('uid')
    def validate_uid(cls, v):
        length_validator('uid', v, 36)
        return

    @validator('contract_id')
    def validate_contract_id(cls, v):
        length_validator('contract_id', v, 36)
        return v

    @validator('visual_number')
    def validate_visual_number(cls, v):
        length_validator('visual_number', v, 64)
        return v

    @validator('issuer')
    def validate_issuer(cls, v):
        length_validator('issuer', v, 64)
        return v

    @validator('group_id')
    def validate_group_id(cls, v):
        length_validator('group_id', v, 36)
        return v

    @validator('language')
    def validate_language(cls, v):
        length_validator('language', v, 2)
        return v


class AuthorizationInfo(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/master/mod_tokens.asciidoc#131-authorizationinfo-object
    """
    allowed: AllowedType
    token: Token
    location: Optional[LocationReference]
    authorization_reference: Optional[CiString]
    info = Optional[DisplayText]

    @validator('authorization_reference')
    def validate_authorization_reference(cls, v):
        length_validator('authorization_reference', v, 36)
        return v
