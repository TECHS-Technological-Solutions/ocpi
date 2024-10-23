from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator

from py_ocpi.core.logs import LoggingConfig, logger


class Settings(BaseSettings):
    ENVIRONMENT: str = "production"
    NO_AUTH: bool = False
    PROJECT_NAME: str = "OCPI"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    OCPI_HOST: str = "www.example.com"
    OCPI_PREFIX: str = "ocpi"
    PUSH_PREFIX: str = "push"
    COUNTRY_CODE: str = "US"
    PARTY_ID: str = "NON"
    PROTOCOL: str = "https"
    COMMAND_AWAIT_TIME: int = 5
    GET_ACTIVE_PROFILE_AWAIT_TIME: int = 5
    TRAILING_SLASH: bool = True

    @classmethod
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(
        cls, v: Union[str, List[str]]
    ) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()

logging_config = LoggingConfig(settings.ENVIRONMENT, logger)
logging_config.configure_logger()
