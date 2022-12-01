from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient

from py_ocpi import get_application
from py_ocpi.core import enums
from py_ocpi.modules.versions.enums import VersionNumber


def test_inject_dependency():
    crud = AsyncMock()
    crud.list.return_value = [], 0, True

    adapter = MagicMock()

    app = get_application([VersionNumber.v_2_2_1], [enums.RoleEnum.cpo], crud, adapter)

    client = TestClient(app)
    client.get('/ocpi/cpo/2.2.1/locations')

    crud.list.assert_awaited_once()
