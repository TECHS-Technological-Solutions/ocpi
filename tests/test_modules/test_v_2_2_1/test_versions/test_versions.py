from fastapi.testclient import TestClient

from py_ocpi.main import get_application
from py_ocpi.core import enums
from py_ocpi.core.crud import Crud
from py_ocpi.modules.versions.enums import VersionNumber

from tests.test_modules.utils import AUTH_TOKEN, ClientAuthenticator
from .test_utils import AUTH_HEADERS, WRONG_AUTH_HEADERS

VERSIONS_URL = "/ocpi/versions"
VERSION_URL = "/ocpi/2.2.1/details"


def test_get_versions():
    class MockCrud(Crud):
        @classmethod
        async def do(cls, *args, **kwargs):
            return AUTH_TOKEN

    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[],
    )
    client = TestClient(app)

    response = client.get(
        VERSIONS_URL,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 1


def test_get_versions_not_authenticated():
    class MockCrud(Crud):
        @classmethod
        async def do(cls, *args, **kwargs):
            return None

    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[],
    )
    client = TestClient(app)

    response = client.get(
        VERSIONS_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 401


def test_get_versions_v_2_2_1():
    class MockCrud(Crud):
        @classmethod
        async def do(cls, *args, **kwargs):
            return AUTH_TOKEN

    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[],
    )
    client = TestClient(app)

    response = client.get(
        VERSION_URL,
        headers=AUTH_HEADERS,
    )

    assert response.status_code == 200
    assert len(response.json()["data"]) == 2


def test_get_versions_v_2_2_1_not_authenticated():
    class MockCrud(Crud):
        @classmethod
        async def do(cls, *args, **kwargs):
            return None

    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=MockCrud,
        authenticator=ClientAuthenticator,
        modules=[],
    )
    client = TestClient(app)

    response = client.get(
        VERSION_URL,
        headers=WRONG_AUTH_HEADERS,
    )

    assert response.status_code == 401
