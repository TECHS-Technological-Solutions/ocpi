from datetime import datetime

from fastapi import Query

from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.authenticator import Authenticator
from py_ocpi.core.config import settings
from py_ocpi.core.crud import Crud
from py_ocpi.core.data_types import URL
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.versions.schemas import Version


def get_crud():
    return Crud


def get_adapter():
    return Adapter


def get_authenticator():
    return Authenticator


def get_versions():
    return [
        Version(
            version=VersionNumber.v_2_2_1,
            url=URL(
                f"https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/"
                f"{VersionNumber.v_2_2_1.value}/details"
            ),
        ).dict(),
    ]


def get_endpoints():
    return {}


def get_modules():
    return []


def pagination_filters(
    date_from: datetime = Query(default=None),
    date_to: datetime = Query(default=None),
    offset: int = Query(default=0),
    limit: int = Query(default=50),
):
    return {
        "date_from": date_from,
        "date_to": date_to,
        "offset": offset,
        "limit": limit,
    }
