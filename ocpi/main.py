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
    versions_router
)
cpo_router.include_router(
    locations_cpo_2_2_1_router
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
