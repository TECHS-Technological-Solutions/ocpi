from py_ocpi.locations.v_2_2_1.schemas import Location
from py_ocpi.credentials.v_2_2_1.schemas import Credentials
from py_ocpi.cdrs.v_2_2_1.schemas import Cdr
from py_ocpi.sessions.v_2_2_1.enums import ChargingPreferencesResponse


class Adapter:
    @classmethod
    def location_adapter(cls, data) -> Location:
        ...

    @classmethod
    def session_adapter(cls, data) -> Location:
        ...

    @classmethod
    def charging_preference_adapter(cls, data) -> ChargingPreferencesResponse:
        ...

    @classmethod
    def credentials_adapter(cls, data) -> Credentials:
        ...

    @classmethod
    def cdr_adapter(cls, data) -> Cdr:
        ...

    @classmethod
    def commands_adapter(cls, data):
        ...

    @classmethod
    def token_adapter(cls, data) -> Cdr:
        ...
