from typing import Optional, List
from pydantic import BaseModel

from py_ocpi.core.data_types import String, CiString, DisplayText, DateTime
from py_ocpi.tokens.v_2_2_1.enums import AllowedType, TokenType, WhitelistType
from py_ocpi.sessions.v_2_2_1.enums import ProfileType


class EnergyContract(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tokens.asciidoc#142-energycontract-class
    """
    supplier_name: String(64)
    contract_id: Optional[String(64)]


class LocationReference(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tokens.asciidoc#143-locationreferences-class
    """
    location_id: CiString(36)
    evse_uids: List[CiString(36)] = []


class Token(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tokens.asciidoc#132-token-object
    """
    country_code: CiString(2)
    party_id: CiString(3)
    uid: CiString(36)
    type: TokenType
    contract_id: CiString(36)
    visual_number: Optional[String(64)]
    issuer: String(64)
    group_id: Optional[CiString(36)]
    valid: bool
    whitelist: WhitelistType
    language: Optional[String(2)]
    default_profile_type: Optional[ProfileType]
    energy_contract: Optional[EnergyContract]
    last_updated: DateTime


class TokenUpdate(BaseModel):
    country_code: Optional[CiString(2)]
    party_id: Optional[CiString(3)]
    uid: Optional[CiString(36)]
    type: Optional[TokenType]
    contract_id: Optional[CiString(36)]
    visual_number: Optional[String(64)]
    issuer: Optional[String(64)]
    group_id: Optional[CiString(36)]
    valid: Optional[bool]
    whitelist: Optional[WhitelistType]
    language: Optional[String(2)]
    default_profile_type: Optional[ProfileType]
    energy_contract: Optional[EnergyContract]
    last_updated: DateTime


class AuthorizationInfo(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tokens.asciidoc#131-authorizationinfo-object
    """
    allowed: AllowedType
    token: Token
    location: Optional[LocationReference]
    authorization_reference: Optional[CiString(36)]
    info: Optional[DisplayText]
