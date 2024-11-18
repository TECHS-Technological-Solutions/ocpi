import pytest

from fastapi.testclient import TestClient

from py_ocpi.main import get_application
from py_ocpi.core import enums
from py_ocpi.modules.versions.enums import VersionNumber

from .utils import Crud, ClientAuthenticator


@pytest.fixture
def token_cpo_v_2_2_1():
    return get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.tokens],
    )


@pytest.fixture
def token_emsp_v_2_2_1():
    return get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.emsp],
        crud=Crud,
        authenticator=ClientAuthenticator,
        modules=[enums.ModuleID.tokens],
    )


@pytest.fixture
def client_cpo_v_2_2_1(token_cpo_v_2_2_1):
    return TestClient(token_cpo_v_2_2_1)


@pytest.fixture
def client_emsp_v_2_2_1(token_emsp_v_2_2_1):
    return TestClient(token_emsp_v_2_2_1)
