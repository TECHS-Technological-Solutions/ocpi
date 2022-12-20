from uuid import uuid4

from fastapi.testclient import TestClient

from py_ocpi.main import get_application
from py_ocpi.core import enums
from py_ocpi.core.config import settings
from py_ocpi.core.crud import Crud
from py_ocpi.core.adapter import Adapter
from py_ocpi.modules.locations.v_2_2_1.schemas import Location
from py_ocpi.modules.versions.enums import VersionNumber


def test_get_versions():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.get('/ocpi/versions')

    assert response.status_code == 200
    assert len(response.json()['data']) == 1


def test_get_versions_v_2_2_1():

    app = get_application(VersionNumber.v_2_2_1, [enums.RoleEnum.cpo], Crud, Adapter)

    client = TestClient(app)
    response = client.get('/ocpi/2.2.1/details')

    assert response.status_code == 200
    assert response.json()['data'][0]['version'] == '2.2.1'
