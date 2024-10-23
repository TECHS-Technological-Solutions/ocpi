from abc import ABC, abstractmethod

from typing import List

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
            logger.debug("Given `%s` token is not valid" % auth_token)
            raise AuthorizationOCPIError

    @classmethod
    async def authenticate_credentials(
        cls,
        auth_token: str,
    ) -> str | dict | None:
        """Authenticate given auth token where both tokens valid."""
        if auth_token:
            list_token_a = await cls.get_valid_token_a()
            if auth_token in list_token_a:
                logger.debug("Token A `%s` is used." % auth_token)
                return {}

            list_token_c = await cls.get_valid_token_c()
            if auth_token in list_token_c:
                logger.debug("Token C `%s` is used." % auth_token)
                return auth_token
        logger.debug("Token `%s` is not of type A or C." % auth_token)
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
