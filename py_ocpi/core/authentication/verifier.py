from fastapi import (
    Depends,
    Header,
    Path,
    Security,
    status,
    Query,
    WebSocketException,
)
from fastapi.security import APIKeyHeader

from py_ocpi.core.authentication.authenticator import Authenticator
from py_ocpi.core.config import logger, settings
from py_ocpi.core.dependencies import get_authenticator
from py_ocpi.core.exceptions import AuthorizationOCPIError
from py_ocpi.core.utils import decode_string_base64
from py_ocpi.modules.versions.enums import VersionNumber

api_key_header = APIKeyHeader(
    name="authorization",
    description="API key with `Token ` prefix.",
    scheme_name="Token",
)
auth_verifier = Security(api_key_header) if not settings.NO_AUTH else ""


class AuthorizationVerifier:
    """
    A class responsible for verifying authorization tokens
    based on the specified version number.

    :param version (VersionNumber): OCPI version used.
    """

    def __init__(self, version: VersionNumber) -> None:
        self.version = version

    async def __call__(
        self,
        authorization: str = auth_verifier,
        authenticator: Authenticator = Depends(get_authenticator),
    ):
        """
        Verifies the authorization token using the specified version
        and an Authenticator.

        :param authorization (str): The authorization header containing
          the token.
        :param authenticator (Authenticator): An Authenticator instance used
          for authentication.

        :raises AuthorizationOCPIError: If there is an issue with
          the authorization token.
        """
        if settings.NO_AUTH and authorization == "":
            logger.debug("Authentication skipped due to NO_AUTH setting.")
            return True

        try:
            token = authorization.split()[1]
            if self.version.startswith("2.2"):
                try:
                    token = decode_string_base64(token)
                except UnicodeDecodeError:
                    logger.debug(
                        "Token `%s` cannot be decoded. "
                        "Check if the token is already encoded." % token
                    )
                    raise AuthorizationOCPIError
            await authenticator.authenticate(token)
        except IndexError:
            logger.debug(
                "Token `%s` cannot be split in parts. "
                "Check if it starts with `Token `"
            )
            raise AuthorizationOCPIError


class CredentialsAuthorizationVerifier:
    """
    A class responsible for verifying authorization tokens
    based on the specified version number.

    :param version (VersionNumber): OCPI version used.
    """

    def __init__(self, version: VersionNumber | None) -> None:
        self.version = version

    async def __call__(
        self,
        authorization: str = Security(api_key_header),
        authenticator: Authenticator = Depends(get_authenticator),
    ) -> str | dict | None:
        """
        Verifies the authorization token using the specified version
        and an Authenticator.

        :param authorization (str): The authorization header containing
          the token.
        :param authenticator (Authenticator): An Authenticator instance used
          for authentication.

        :raises AuthorizationOCPIError: If there is an issue with
          the authorization token.
        """
        try:
            token = authorization.split()[1]
        except IndexError:
            logger.debug(
                "Token `%s` cannot be split in parts. "
                "Check if it starts with `Token `"
            )
            raise AuthorizationOCPIError

        if self.version:
            if self.version.startswith("2.2"):
                try:
                    token = decode_string_base64(token)
                except UnicodeDecodeError:
                    logger.debug(
                        "Token `%s` cannot be decoded. "
                        "Check if the token is already encoded." % token
                    )
                    raise AuthorizationOCPIError
        else:
            try:
                token = decode_string_base64(token)
            except UnicodeDecodeError:
                pass
        return await authenticator.authenticate_credentials(token)


class VersionsAuthorizationVerifier(CredentialsAuthorizationVerifier):
    """
    A class responsible for verifying authorization tokens
    based on the specified version number.
    """

    async def __call__(
        self,
        authorization: str = auth_verifier,
        authenticator: Authenticator = Depends(get_authenticator),
    ) -> str | dict | None:
        """
        Verifies the authorization token using the specified version
        and an Authenticator for version endpoints.

        :param authorization (str): The authorization header containing
          the token.
        :param authenticator (Authenticator): An Authenticator instance used
          for authentication.

        :raises AuthorizationOCPIError: If there is an issue with
          the authorization token.
        """
        if settings.NO_AUTH and authorization == "":
            logger.debug("Authentication skipped due to NO_AUTH setting.")
            return ""
        return await super().__call__(authorization, authenticator)


class HttpPushVerifier:
    """
    A class responsible for verifying authorization tokens if using push.
    """

    async def __call__(
        self,
        authorization: str = Header(...) if not settings.NO_AUTH else "",
        version: VersionNumber = Path(...),
        authenticator: Authenticator = Depends(get_authenticator),
    ):
        """
        Verifies the authorization token using the specified version
        and an Authenticator.

        :param authorization (str): The authorization header containing
          the token.
        :param version (VersionNumber): The authorization header containing
          the token.
        :param authenticator (Authenticator): An Authenticator instance used
          for authentication.

        :raises AuthorizationOCPIError: If there is an issue with
          the authorization token.
        """
        if settings.NO_AUTH and authorization == "":
            logger.debug("Authentication skipped due to NO_AUTH setting.")
            return True

        try:
            token = authorization.split()[1]
            if version.value.startswith("2.2"):
                try:
                    token = decode_string_base64(token)
                except UnicodeDecodeError:
                    logger.debug(
                        "Token `%s` cannot be decoded. "
                        "Check if the token is already encoded." % token
                    )
                    raise AuthorizationOCPIError
            await authenticator.authenticate(token)
        except IndexError:
            logger.debug(
                "Token `%s` cannot be split in parts. "
                "Check if it starts with `Token `"
            )
            raise AuthorizationOCPIError


class WSPushVerifier:
    """
    A class responsible for verifying authorization tokens if using ws push.
    """

    async def __call__(
        self,
        token: str = Query(...) if not settings.NO_AUTH else "",
        version: VersionNumber = Path(...),
        authenticator: Authenticator = Depends(get_authenticator),
    ):
        """
        Verifies the authorization token using the specified version
        and an Authenticator.

        :param token (str): Token parameter in ws.
        :param version (str): The authorization header containing
          the token.
        :param authenticator (Authenticator): An Authenticator instance used
          for authentication.

        :raises AuthorizationOCPIError: If there is an issue with
          the authorization token.
        """
        if settings.NO_AUTH and token == "":
            logger.debug("Authentication skipped due to NO_AUTH setting.")
            return True

        try:
            if not token:
                logger.debug("Token wasn't given.")
                raise AuthorizationOCPIError

            if version.value.startswith("2.2"):
                try:
                    token = decode_string_base64(token)
                except UnicodeDecodeError:
                    logger.debug(
                        "Token `%s` cannot be decoded. "
                        "Check if the token is already encoded." % token
                    )
                    raise AuthorizationOCPIError
            await authenticator.authenticate(token)
        except AuthorizationOCPIError:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
