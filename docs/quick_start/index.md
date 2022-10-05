# Quick Start

## CRUD
Create a crud class with get, list, create, update and delete methods:

```python
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
```

## Adapter
Create a adapter class with an adapter method for each OCPI module. this example will only include the adapter for locations module.

```python
class Adapter:
    @classmethod
    def location_adapter(cls, data) -> Location:
        return Location(**data)
```

## Create Application
Specify the OCPI versions and OCPI roles that are intended for the application and pass the already defined Crud and Adapter.

```python
app = get_application([VersionNumber.v_2_2_1], [enums.RoleEnum.cpo], Crud, Adapter)
```

## Run Application
The app is and instance of FastAPI app. you can run this app like any FastAPI app is run.
