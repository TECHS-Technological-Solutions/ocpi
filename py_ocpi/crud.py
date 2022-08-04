from py_ocpi.core.enums import ModuleID


class CRUD:
    @classmethod
    async def get(cls, module: ModuleID, id):
        pass

    @classmethod
    async def list(cls, module: ModuleID) -> list:
        pass

    @classmethod
    async def create(cls, module: ModuleID, data):
        pass

    @classmethod
    async def update(cls, module: ModuleID, data):
        pass

    @classmethod
    async def delete(cls, module: ModuleID, id):
        pass


def get_crud():
    return CRUD
