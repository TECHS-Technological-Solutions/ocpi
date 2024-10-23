from typing import Optional, List
from pydantic import BaseModel

from py_ocpi.core.data_types import String, DisplayText, DateTime
from py_ocpi.modules.tokens.v_2_1_1.enums import (
    Allowed,
    TokenType,
    WhitelistType,
)


class LocationReference(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tokens.md#42-locationreferences-class
    """

    location_id: String(39)  # type: ignore
    evse_uids: List[String(39)] = []  # type: ignore
    connector_ids: List[String(36)] = []  # type: ignore


class Token(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tokens.md#32-token-object
    """

    uid: String(36)  # type: ignore
    type: TokenType
    auth_id: String(36)  # type: ignore
    visual_number: Optional[String(64)]  # type: ignore
    issuer: String(64)  # type: ignore
    valid: bool
    whitelist: WhitelistType
    language: Optional[String(2)]  # type: ignore
    last_updated: DateTime


class TokenPartialUpdate(BaseModel):
    uid: Optional[String(36)]  # type: ignore
    type: Optional[TokenType]
    auth_id: Optional[String(36)]  # type: ignore
    visual_number: Optional[String(64)]  # type: ignore
    issuer: Optional[String(64)]  # type: ignore
    valid: Optional[bool]
    whitelist: Optional[WhitelistType]
    language: Optional[String(2)]  # type: ignore
    last_updated: Optional[DateTime]


class AuthorizationInfo(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_tokens.md#31-authorizationinfo-object
    """

    allowed: Allowed
    location: Optional[LocationReference]
    info: Optional[DisplayText]
