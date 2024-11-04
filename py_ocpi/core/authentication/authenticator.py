from abc import ABC, abstractmethod

from typing import List, Union

from py_ocpi.core.exceptions import AuthorizationOCPIError
from py_ocpi.core.config import logger


class Authenticator(ABC):
    """Base class responsible for verifying authorization tokens."""

    @classmethod
    async def authenticate(cls, auth_token: str) -> None:
        """Authenticate given auth token.

        :raises AuthorizationOCPIError: If auth_token is not in a given
          list of verified tokens C.
        """
        list_token_c = await cls.get_valid_token_c()
        if auth_token not in list_token_c:
            logger.debug(f"Given `{auth_token}` token is not valid")
            raise AuthorizationOCPIError

    @classmethod
    async def authenticate_credentials(
        cls,
        auth_token: str,
    ) -> Union[str, dict, None]:
        """Authenticate given auth token where both tokens valid."""
        if auth_token:
            list_token_a = await cls.get_valid_token_a()
            if auth_token in list_token_a:
                logger.debug(f"Token A `{auth_token}` is used.")
                return {}

            list_token_c = await cls.get_valid_token_c()
            if auth_token in list_token_c:
                logger.debug(f"Token C `{auth_token}` is used.")
                return auth_token
        logger.debug(f"Token `{auth_token}` is not of type A or C.")
        return None

    @classmethod
    @abstractmethod
    async def get_valid_token_c(cls) -> List[str]:
        """Return valid token c list."""
        pass

    @classmethod
    @abstractmethod
    async def get_valid_token_a(cls) -> List[str]:
        """Return valid token a list."""
        pass
