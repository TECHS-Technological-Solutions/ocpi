from typing import List, Union

from pydantic import AnyHttpUrl, BaseSettings, validator


class Settings(BaseSettings):
    PROJECT_NAME: str = 'OCPI'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    OCPI_HOST: str = 'www.example.com'
    OCPI_PREFIX: str = 'ocpi'

    @classmethod
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        if isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
