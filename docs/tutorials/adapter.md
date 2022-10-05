# Adapter
adapter function will adapt the result from Crud to acceptable schema by OCPI.  
each module in OCPI must have a corresponding method in adapter.  
for example the adapter for location module is _location_adapter_.

```python
class Adapter:
    @classmethod
    def location_adapter(cls, data) -> Location:
        return Location(**data)
```