from py_ocpi.locations.v_2_2_1.schemas import Location
from py_ocpi.credentials.v_2_2_1.schemas import Credentials


class Adapter:
    @classmethod
    def location_adapter(cls, data) -> Location:
        pass

    @classmethod
    def credentials_adapter(cls, data) -> Credentials:
        pass


def get_adapter():
    return Adapter
