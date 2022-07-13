from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from ocpi.credentials.api import credentials_cpo_2_2_1_router
from ocpi.versions.api import versions_cpo_2_2_1_router
from ocpi.sessions.api import sessions_cpo_2_2_1_router
from ocpi.commands.api import commands_cpo_2_2_1_router
from ocpi.tariffs.api import tariffs_cpo_2_2_1_router
from ocpi.tokens.api import tokens_cpo_2_2_1_router
from ocpi.cdrs.api import cdrs_cpo_2_2_1_router
from ocpi.core.config import settings


def get_application():
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return _app


app = get_application()

cpo_router = APIRouter(
)
cpo_router.include_router(
    versions_cpo_2_2_1_router
)
cpo_router.include_router(
    credentials_cpo_2_2_1_router
)
cpo_router.include_router(
    sessions_cpo_2_2_1_router
)
cpo_router.include_router(
    commands_cpo_2_2_1_router
)
cpo_router.include_router(
    tariffs_cpo_2_2_1_router
)
cpo_router.include_router(
    tokens_cpo_2_2_1_router
)
cpo_router.include_router(
    cdrs_cpo_2_2_1_router
)

app.include_router(
    cpo_router,
    prefix='/cpo',
    tags=['CPO']
)
