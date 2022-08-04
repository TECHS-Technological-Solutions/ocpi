from py_ocpi.locations.v_2_2_1.schemas import Location


class Adapter:
    @classmethod
    def location_adapter(cls, data) -> Location:
        pass


def get_adapter():
    return Adapter
