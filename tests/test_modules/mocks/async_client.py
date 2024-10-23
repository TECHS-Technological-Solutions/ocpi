from py_ocpi.core.dependencies import get_versions
from py_ocpi.core.endpoints import ENDPOINTS
from py_ocpi.core.enums import RoleEnum, ModuleID
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.versions.v_2_2_1.schemas import VersionDetail

fake_endpoints_data = {
    "data": VersionDetail(
        version=VersionNumber.v_2_2_1,
        endpoints=[
            ENDPOINTS[VersionNumber.v_2_2_1][RoleEnum.cpo][ModuleID.locations]
        ],
    ).dict(),
}

fake_versions_data = {"data": get_versions()}


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


# Connector mocks


class MockAsyncClientVersionsAndEndpoints:
    async def get(url, headers):
        if url == "versions_url":
            return MockResponse(fake_versions_data, 200)
        else:
            return MockResponse(fake_endpoints_data, 200)

    def build_request(self, request, headers, json):
        return self

    async def send(request):
        return MockResponse(fake_endpoints_data, 200)


class MockAsyncClientGeneratorVersionsAndEndpoints:
    async def __aenter__(self):
        return MockAsyncClientVersionsAndEndpoints

    async def __aexit__(self, *args, **kwargs):
        pass
