# CRUD
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
for each OCPI API call, the corresponding method from Crud class will be called. the authentication token used in 
API call is passed to all method calls.

> **_NOTE:_** the list endpoint must return a tuple of **objects list**, **total number of objects** and a boolean identifying whether it's the **last page** or not
