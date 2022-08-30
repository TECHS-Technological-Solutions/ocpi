from typing import Any, Tuple

from py_ocpi.core.enums import ModuleID


class Crud:
    @classmethod
    async def get(cls, module: ModuleID, id, *args, **kwargs) -> Any:
        ...

    @classmethod
    async def list(cls, module: ModuleID, filters: dict, *args, **kwargs) -> Tuple[list, int, bool]:
        ...

    @classmethod
    async def create(cls, module: ModuleID, data, *args, **kwargs) -> Any:
        ...

    @classmethod
    async def update(cls, module: ModuleID, data, id, *args, **kwargs) -> Any:
        ...

    @classmethod
    async def delete(cls, module: ModuleID, id, *args, **kwargs) -> Any:
        ...
