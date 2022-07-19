from ocpi.core.v_2_2_1.enums import ModuleID


class CRUD:
    @classmethod
    def get(cls, module: ModuleID, id):
        pass

    @classmethod
    def list(cls, module: ModuleID) -> list:
        pass

    @classmethod
    def create(cls, module: ModuleID, data):
        pass

    @classmethod
    def update(cls, module: ModuleID, data):
        pass

    @classmethod
    def delete(cls, module: ModuleID, id):
        pass
