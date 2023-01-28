from typing import Any, List

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from py_ocpi.modules.versions.api import router as versions_router, versions_v_2_2_1_router
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.versions.schemas import Version
from py_ocpi.core.dependencies import get_crud, get_adapter, get_versions
from py_ocpi.core import status
from py_ocpi.core.enums import RoleEnum
from py_ocpi.core.config import settings
from py_ocpi.core.data_types import URL
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.exceptions import AuthorizationOCPIError, NotFoundOCPIError
from py_ocpi.core.push import http_router as http_push_router, websocket_router as websocket_push_router
from py_ocpi.routers import v_2_2_1_cpo_router, v_2_2_1_emsp_router


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        try:
            response = await call_next(request)
        except AuthorizationOCPIError as e:
            raise HTTPException(403, str(e)) from e
        except NotFoundOCPIError as e:
            raise HTTPException(404, str(e)) from e
        except ValidationError:
            response = JSONResponse(
                OCPIResponse(
                    data=[],
                    **status.OCPI_3000_GENERIC_SERVER_ERROR,
                ).dict()
            )
        return response


def get_application(
    version_numbers: List[VersionNumber],
    roles: List[RoleEnum],
    crud: Any,
    adapter: Any,
    http_push: bool = False,
    websocket_push: bool = False,
) -> FastAPI:
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url=f'/{settings.OCPI_PREFIX}/docs',
        openapi_url=f"/{settings.OCPI_PREFIX}/openapi.json"
    )

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    _app.add_middleware(ExceptionHandlerMiddleware)

    _app.include_router(
        versions_router,
        prefix=f'/{settings.OCPI_PREFIX}',
    )

    if http_push:
        _app.include_router(
            http_push_router,
            prefix=f'/{settings.PUSH_PREFIX}',
        )

    if websocket_push:
        _app.include_router(
            websocket_push_router,
            prefix=f'/{settings.PUSH_PREFIX}',
        )

    versions = []

    if VersionNumber.v_2_2_1 in version_numbers:
        _app.include_router(
            versions_v_2_2_1_router,
            prefix=f'/{settings.OCPI_PREFIX}',
        )

        if RoleEnum.cpo in roles:
            _app.include_router(
                v_2_2_1_cpo_router,
                prefix=f'/{settings.OCPI_PREFIX}/cpo/{VersionNumber.v_2_2_1.value}',
                tags=['CPO']
            )

            versions.append(
                Version(
                    version=VersionNumber.v_2_2_1,
                    url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo/{VersionNumber.v_2_2_1.value}/')
                ).dict(),
            )

        if RoleEnum.emsp in roles:
            _app.include_router(
                v_2_2_1_emsp_router,
                prefix=f'/{settings.OCPI_PREFIX}/emsp/{VersionNumber.v_2_2_1.value}',
                tags=['EMSP']
            )

            versions.append(
                Version(
                    version=VersionNumber.v_2_2_1,
                    url=URL(f'https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/emsp/{VersionNumber.v_2_2_1.value}/')
                ).dict(),
            )

    def override_get_crud():
        return crud

    _app.dependency_overrides[get_crud] = override_get_crud

    def override_get_adapter():
        return adapter

    _app.dependency_overrides[get_adapter] = override_get_adapter

    def override_get_versions():
        return versions

    _app.dependency_overrides[get_versions] = override_get_versions

    return _app
