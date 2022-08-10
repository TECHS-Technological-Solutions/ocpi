from typing import Any, Tuple

from py_ocpi.core.enums import ModuleID


class CRUD:
    @classmethod
    async def get(cls, module: ModuleID, id) -> Any:
        pass

    @classmethod
    async def list(cls, module: ModuleID, filters: dict) -> Tuple[list, int, bool]:
        pass

    @classmethod
    async def create(cls, module: ModuleID, data) -> Any:
        pass

    @classmethod
    async def update(cls, module: ModuleID, data) -> Any:
        pass

    @classmethod
    async def delete(cls, module: ModuleID, id) -> Any:
        pass


def get_crud():
    return CRUD
