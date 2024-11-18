import pytest

from fastapi.testclient import TestClient

from py_ocpi.main import get_application
from py_ocpi.core import enums
from py_ocpi.modules.versions.enums import VersionNumber

from tests.test_modules.utils import ClientAuthenticator

from .utils import Crud


@pytest.fixture
def clientinfo_cpo_v_2_2_1():
    return get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.hub_client_info],
    )


@pytest.fixture
def clientinfo_emsp_v_2_2_1():
    return get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.hub_client_info],
    )


@pytest.fixture
def client_cpo_v_2_2_1(clientinfo_cpo_v_2_2_1):
    return TestClient(clientinfo_cpo_v_2_2_1)


@pytest.fixture
def client_emsp_v_2_2_1(clientinfo_emsp_v_2_2_1):
    return TestClient(clientinfo_emsp_v_2_2_1)
