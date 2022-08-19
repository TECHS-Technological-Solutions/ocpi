from datetime import datetime, timezone

from pydantic import BaseModel

from py_ocpi.core.data_types import String, DateTime


class OCPIResponse(BaseModel):
    data: list
    status_code: int
    status_message: String(255)
    timestamp: DateTime = str(datetime.now(timezone.utc))
