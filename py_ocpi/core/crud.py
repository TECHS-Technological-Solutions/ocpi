from typing import Any, Literal, Tuple

from py_ocpi.core.enums import ModuleID, Action


class Crud:
    @classmethod
    async def get(cls, module: ModuleID, id, *args, **kwargs) -> Any:
        """Get an object

        Args:
            module (ModuleID): The OCPI module
            id (Any): The ID of the object

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module
            party_id (CiString(3)): The party ID (used in Tokens module)
            token_uid (CiString(36)): The token UID (used in Tokens module)
            token_type (TokenType): The token type (used in Tokens module)

        Returns:
            Any: The object data
        """

    @classmethod
    async def list(cls, module: ModuleID, filters: dict, *args, **kwargs) -> Tuple[list, int, bool]:
        """Get the list of objects

        Args:
            module (ModuleID): The OCPI module
            filters (dict): OCPI pagination filters

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module

        Returns:
            Tuple[list, int, bool]: Objects list, Total number of objects, if it's the last page or not(for pagination)
        """

    @classmethod
    async def create(cls, module: ModuleID, data: dict, *args, **kwargs) -> Any:
        """Create an object

        Args:
            module (ModuleID): The OCPI module
            data (dict): The object details

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module
            command (CommandType): The command type (used in Commands module)
            party_id (CiString(3)): The party ID (used in Tokens module)
            token_uid (CiString(36)): The token UID (used in Tokens module)
            token_type (TokenType): The token type (used in Tokens module)

        Returns:
            Any: The created object data
        """

    @classmethod
    async def update(cls, module: ModuleID, data: dict, id, *args, **kwargs) -> Any:
        """Update an object

        Args:
            module (ModuleID): The OCPI module
            data (dict): The object details
            id (Any): The ID of the object

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module
            party_id (CiString(3)): The party ID (used in Tokens module)
            token_uid (CiString(36)): The token UID (used in Tokens module)
            token_type (TokenType): The token type (used in Tokens module)

        Returns:
            Any: The updated object data
        """

    @classmethod
    async def delete(cls, module: ModuleID, id, *args, **kwargs):
        """Delete an object

        Args:
            module (ModuleID): The OCPI module
            id (Any): The ID of the object

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module
        """

    @classmethod
    async def do(cls, module: ModuleID, action: Action, *args, data: dict = None, **kwargs) -> Any:
        """Do an action (non-CRUD)

        Args:
            module (ModuleID): The OCPI module
            action (Action): The action type
            data (dict): The data required for the action

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module

        Returns:
            Any: The action result
        """

    @classmethod
    async def send(cls, module: ModuleID, url: str, method: Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE'],
                   *args, data: dict = None, **kwargs) -> Any:
        """Send a HTTP request

        Args:
            module (ModuleID): The OCPI module
            url (str): The URL to send the request to
            method ('GET', 'POST', 'PUT', 'PATCH', 'DELETE'): _description_
            data (dict, optional): The data used for POST,PATCH or PUT request

        Keyword Args:
            auth_token (str): The authentication token used by third party
            version (VersionNumber): The version number of the caller OCPI module

        Returns:
            Any: The request response
        """
