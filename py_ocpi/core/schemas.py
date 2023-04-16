from datetime import datetime, timezone
from typing import List, Union

from pydantic import BaseModel

from py_ocpi.core.data_types import String, DateTime, URL
from py_ocpi.core.enums import ModuleID


class OCPIResponse(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/transport_and_format.asciidoc#117-response-format
    """
    data: Union[list, dict]
    status_code: int
    status_message: String(255)
    timestamp: DateTime = str(datetime.now(timezone.utc))


class Receiver(BaseModel):
    endpoints_url: URL
    auth_token: str


class Push(BaseModel):
    module_id: ModuleID
    object_id: str
    receivers: List[Receiver]


class ReceiverResponse(BaseModel):
    endpoints_url: URL
    status_code: int
    response: dict


class PushResponse(BaseModel):
    receiver_responses: List[ReceiverResponse]
