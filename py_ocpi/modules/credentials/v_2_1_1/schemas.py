from pydantic import BaseModel

from py_ocpi.core.data_types import URL, String
from py_ocpi.modules.locations.v_2_1_1.schemas import BusinessDetails


class Credentials(BaseModel):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/credentials.md#21-credentials-object
    """

    token: String(64)  # type: ignore
    url: URL
    business_details: BusinessDetails
    party_id: String(3)  # type: ignore
    country_code: String(2)  # type: ignore
