from datetime import datetime

from pydantic import BaseModel

from core.v_2_2_1.data_types import String, DateTime


class OCPIResponse(BaseModel):
    data: dict
    status_code: int
    status_message: String
    timestamp: DateTime = datetime.now()
