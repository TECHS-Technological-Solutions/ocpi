from py_ocpi.locations.v_2_2_1.schemas import Location
from py_ocpi.sessions.v_2_2_1.enums import ChargingPreferencesResponse


class Adapter:
    @classmethod
    def location_adapter(cls, data) -> Location:
        ...

    def session_adapter(cls, data) -> Location:
        ...

    def charging_preference_adapter(cls, data) -> ChargingPreferencesResponse:
        ...


def get_adapter():
    return Adapter
