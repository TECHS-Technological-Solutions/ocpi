from typing import Any, List

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from ocpi.credentials.v_2_2_1.api import cpo_router as credentials_cpo_2_2_1_router
from ocpi.locations.v_2_2_1.api import cpo_router as locations_cpo_2_2_1_router
from ocpi.sessions.v_2_2_1.api import cpo_router as sessions_cpo_2_2_1_router
from ocpi.commands.v_2_2_1.api import cpo_router as commands_cpo_2_2_1_router
from ocpi.tariffs.v_2_2_1.api import cpo_router as tariffs_cpo_2_2_1_router
from ocpi.tokens.v_2_2_1.api import cpo_router as tokens_cpo_2_2_1_router
from ocpi.cdrs.v_2_2_1.api import cpo_router as cdrs_cpo_2_2_1_router
from ocpi.versions.api import router as versions_router
from ocpi.versions.enums import VersionNumber
from ocpi.adapter import get_adapter
from ocpi.crud import get_crud
from ocpi.core.enums import RoleEnum
from ocpi.core.config import settings


def get_application(
    version: VersionNumber,
    roles: List[RoleEnum],
    crud: Any,
    adapter: Any
):
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if version == VersionNumber.v_2_2_1:
        if RoleEnum.CPO in roles:
            _cpo_router = APIRouter(
            )

            _cpo_router.include_router(
                versions_router
            )
            _cpo_router.include_router(
                locations_cpo_2_2_1_router
            )
            _cpo_router.include_router(
                credentials_cpo_2_2_1_router
            )
            _cpo_router.include_router(
                sessions_cpo_2_2_1_router
            )
            _cpo_router.include_router(
                commands_cpo_2_2_1_router
            )
            _cpo_router.include_router(
                tariffs_cpo_2_2_1_router
            )
            _cpo_router.include_router(
                tokens_cpo_2_2_1_router
            )
            _cpo_router.include_router(
                cdrs_cpo_2_2_1_router
            )

            _app.include_router(
                _cpo_router,
                prefix='/cpo',
                tags=['CPO']
            )

    def override_get_crud():
        return crud

    _app.dependency_overrides[get_crud] = override_get_crud

    def override_get_adapter():
        return adapter

    _app.dependency_overrides[get_adapter] = override_get_adapter

    return _app
