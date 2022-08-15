from typing import Any, Tuple

from py_ocpi.core.enums import ModuleID


class CRUD:
    @classmethod
    async def get(cls, module: ModuleID, id) -> Any:
        ...

    @classmethod
    async def list(cls, module: ModuleID, filters: dict) -> Tuple[list, int, bool]:
        ...

    @classmethod
    async def create(cls, module: ModuleID, data) -> Any:
        ...

    @classmethod
    async def update(cls, module: ModuleID, data, id) -> Any:
        ...

    @classmethod
    async def delete(cls, module: ModuleID, id) -> Any:
        ...


def get_crud():
    return CRUD
