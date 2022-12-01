from py_ocpi.core.dependencies import get_versions

fake_versions_and_endpoints_data = {
    'data': get_versions()
}


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


# Connector mocks

class MockAsyncClientVersionsAndEndpoints:
    async def get(request, headers):
        return MockResponse(fake_versions_and_endpoints_data, 200)


class MockAsyncClientGeneratorVersionsAndEndpoints:

    async def __aenter__(self):
        return MockAsyncClientVersionsAndEndpoints

    async def __aexit__(self, *args, **kwargs):
        pass
