from typing import Any, List

from fastapi import FastAPI, Request, status as fastapistatus
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from starlette.middleware.base import (
    BaseHTTPMiddleware,
    RequestResponseEndpoint,
)
from py_ocpi.core.endpoints import ENDPOINTS

from py_ocpi.modules.versions import router as versions_router
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.versions.schemas import Version
from py_ocpi.core.dependencies import (
    get_crud,
    get_adapter,
    get_versions,
    get_endpoints,
    get_modules,
    get_authenticator,
)
from py_ocpi.core import status
from py_ocpi.core.adapter import BaseAdapter
from py_ocpi.core.enums import RoleEnum, ModuleID
from py_ocpi.core.config import settings, logger
from py_ocpi.core.data_types import URL
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.exceptions import AuthorizationOCPIError, NotFoundOCPIError
from py_ocpi.core.push import (
    http_router as http_push_router,
    websocket_router as websocket_push_router,
)
from py_ocpi.core.routers import ROUTERS


class ExceptionHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ):
        logger.debug("%s: %s" % (request.method, request.url))
        logger.debug("Request headers - %s" % request.headers)

        try:
            response = await call_next(request)
        except AuthorizationOCPIError as e:
            logger.warning("OCPI middleware AuthorizationOCPIError exception.")
            response = JSONResponse(
                content={"detail": str(e)},
                status_code=fastapistatus.HTTP_403_FORBIDDEN,
            )
        except NotFoundOCPIError as e:
            logger.warning("OCPI middleware NotFoundOCPIError exception.")
            response = JSONResponse(
                content={"detail": str(e)},
                status_code=fastapistatus.HTTP_404_NOT_FOUND,
            )
        except ValidationError:
            logger.warning("OCPI middleware ValidationError exception.")
            response = JSONResponse(
                OCPIResponse(
                    data=[],
                    **status.OCPI_3000_GENERIC_SERVER_ERROR,
                ).dict()
            )
        except Exception as e:
            logger.warning(f"Unknown exception: {str(e)}.")
            response = JSONResponse(
                OCPIResponse(
                    data=[],
                    **status.OCPI_3000_GENERIC_SERVER_ERROR,
                ).dict()
            )

        logger.debug(f"Response status_code -> {response.status_code}.")
        return response


def get_application(
    version_numbers: List[VersionNumber],
    roles: List[RoleEnum],
    crud: Any,
    modules: List[ModuleID],
    authenticator: Any,
    adapter: Any = BaseAdapter,
    http_push: bool = False,
    websocket_push: bool = False,
) -> FastAPI:
    """
    OCPI application initializer.

    :param version_numbers: List of version numbers which are supported.
    :param roles: Roles which are supported.
    :param crud: Class with crud methods which should contain business logic
      and db methods.
    :param modules: OCPI modules which should be supported. [Some modules are
      related, make sure to check OCPI documentation first.]
    :param authenticator: Authenticator class, which would check validity of
      authentication tokens.
    :param adapter: Model to dict data transformer.
    :param http_push: If True, add endpoint where the command to send to
      corresponding client data update could be made.
    :param websocket_push: If True, add websocket endpoint where data updates
      will be shared.

    :return: FastApi application.
    """
    _app = FastAPI(
        title=settings.PROJECT_NAME,
        docs_url=f"/{settings.OCPI_PREFIX}/docs",
        redoc_url=f"/{settings.OCPI_PREFIX}/redoc",
        openapi_url=f"/{settings.OCPI_PREFIX}/openapi.json",
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
        prefix=f"/{settings.OCPI_PREFIX}",
    )

    if http_push:
        _app.include_router(
            http_push_router,
            prefix=f"/{settings.PUSH_PREFIX}",
        )

    if websocket_push:
        _app.include_router(
            websocket_push_router,
            prefix=f"/{settings.PUSH_PREFIX}",
        )

    versions = []
    version_endpoints: dict[str, list] = {}

    for version in version_numbers:
        mapped_version = ROUTERS.get(version)
        if not mapped_version:
            raise ValueError("Version isn't supported yet.")

        _app.include_router(
            mapped_version["version_router"],
            prefix=f"/{settings.OCPI_PREFIX}",
        )

        versions.append(
            Version(
                version=version,
                url=URL(
                    f"{settings.PROTOCOL}://{settings.OCPI_HOST}/"
                    f"{settings.OCPI_PREFIX}/{version.value}/details"
                ),
            ).dict(),
        )

        version_endpoints[version] = []

        if RoleEnum.cpo in roles:
            for module in modules:
                cpo_router = mapped_version["cpo_router"].get(module)
                if cpo_router:
                    _app.include_router(
                        cpo_router,
                        prefix=f"/{settings.OCPI_PREFIX}/cpo/{version.value}",
                        tags=[f"CPO {version.value}"],
                    )
                    endpoint = ENDPOINTS[version][RoleEnum.cpo].get(module)
                    if endpoint:
                        version_endpoints[version].append(endpoint)

        if RoleEnum.emsp in roles:
            for module in modules:
                emsp_router = mapped_version["emsp_router"].get(module)
                if emsp_router:
                    _app.include_router(
                        emsp_router,
                        prefix=f"/{settings.OCPI_PREFIX}/emsp/{version.value}",
                        tags=[f"EMSP {version.value}"],
                    )
                    endpoint = ENDPOINTS[version][RoleEnum.emsp].get(module)
                    if endpoint:
                        version_endpoints[version].append(endpoint)

    def override_get_crud():
        return crud

    _app.dependency_overrides[get_crud] = override_get_crud

    def override_get_adapter():
        return adapter

    _app.dependency_overrides[get_adapter] = override_get_adapter

    def override_get_versions():
        return versions

    _app.dependency_overrides[get_versions] = override_get_versions

    def override_get_endpoints():
        return version_endpoints

    _app.dependency_overrides[get_endpoints] = override_get_endpoints

    def override_get_modules():
        return modules

    _app.dependency_overrides[get_modules] = override_get_modules()

    def override_get_authenticator():
        return authenticator

    _app.dependency_overrides[get_authenticator] = override_get_authenticator()

    return _app
