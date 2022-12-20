# Quick Start

## CRUD
Create a crud class with get, list, create, update, delete and do methods:

```python
from py_ocpi.core.enums import ModuleID, RoleEnum


class Crud:
    @classmethod
    async def get(cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs) -> Any:
        ...

    @classmethod
    async def list(cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs) -> Tuple[list, int, bool]:
        ...

    @classmethod
    async def create(cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs) -> Any:
        ...

    @classmethod
    async def update(cls, module: ModuleID, role: RoleEnum, data: dict, id, *args, **kwargs) -> Any:
        ...

    @classmethod
    async def delete(cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs):
        ...

    @classmethod
    async def do(cls, module: ModuleID, role: RoleEnum, action: Action, *args, data: dict = None, **kwargs) -> Any:
        ...
```

## Adapter
Create a adapter class with an adapter method for each OCPI module. this example will only include the adapter for locations module.

```python
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.locations.v_2_2_1.schemas import Location


class Adapter:
    @classmethod
    def location_adapter(cls, data: dict, version: VersionNumber = VersionNumber.latest):
        return Location(**data)
```

## Create Application
Specify the OCPI versions and OCPI roles that are intended for the application and pass the already defined Crud and Adapter.

```python
from py_ocpi import get_application

app = get_application([VersionNumber.v_2_2_1], [enums.RoleEnum.cpo], Crud, Adapter)
```

## Run Application
The app is and instance of FastAPI app. you can run it like any FastAPI app.
