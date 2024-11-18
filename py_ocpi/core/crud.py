from typing import Any, Tuple, Optional
from abc import ABC, abstractmethod

from py_ocpi.core.enums import ModuleID, RoleEnum, Action


class Crud(ABC):
    @abstractmethod
    async def get(
        cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs
    ) -> Any:
        """Get an object

        :param module: The OCPI module
        :param role: The role of the caller
        :param id: The ID of the object

        :keyword auth_token: (str) The authentication token used by a third
            party
        :keyword version: (VersionNumber) The version number of the caller
            OCPI module
        :keyword party_id: (CiString(3))  The requested party ID
        :keyword country_code: (CiString(2)) The requested Country code
        :keyword token_type: (TokenType) The token type
        :keyword command: (CommandType) The command type of the OCPP command
        :keyword command_data: Request body of command.
        :keyword session_id: (str) Id of the charging profile corresponding
            session.
        :keyword duration: (int) Length of the requested ActiveChargingProfile
            in seconds.
        :keyword response_url: (str) Url where to send result of the action.
        :keyword charging_profile: (SetChargingProfile) ChargingProfile body.
        :keyword session_id: (str) Id of the charging profile corresponding
            session.

        :return: The object data
        :rtype: Any
        """
        pass

    @abstractmethod
    async def list(
        cls, module: ModuleID, role: RoleEnum, filters: dict, *args, **kwargs
    ) -> Tuple[list, int, bool]:
        """Get the list of objects

        :param module: The OCPI module
        :param role: The role of the caller
        :param filters: OCPI pagination filters

        :keyword auth_token: (str) The authentication token used by a third
            party
        :keyword version: (VersionNumber) The version number of the caller
            OCPI module
        :keyword party_id: (CiString(3))  The requested party ID
        :keyword country_code: (CiString(2)) The requested Country code

        :return:  Objects list, Total number of objects, if
            it's the last page or not(for pagination)
        :rtype: Tuple[list, int, bool]
        """
        pass

    @abstractmethod
    async def create(
        cls, module: ModuleID, role: RoleEnum, data: dict, *args, **kwargs
    ) -> Any:
        """Create an object

        :param module: The OCPI module
        :param role: The role of the caller
        :param data: The object details

        :keyword auth_token: (str) The authentication token used by
            a third party
        :keyword version: (VersionNumber) The version number of the caller
            OCPI module
        :keyword party_id: (CiString(3))  The requested party ID
        :keyword country_code: (CiString(2)) The requested Country code
        :keyword token_type: (TokenType) The token type
        :keyword command: (CommandType) The command type of the OCPP command
        :keyword query_params: (dict) Charging profile request query params.

        :return: The created object data
        :rtype: Any
        """
        pass

    @abstractmethod
    async def update(
        cls,
        module: ModuleID,
        role: RoleEnum,
        data: dict,
        id: Any,
        *args,
        **kwargs,
    ) -> Any:
        """Update an object

        :param module: The OCPI module
        :param role: The role of the caller
        :param data: The object details
        :param id: The ID of the object

        :keyword auth_token: (str) The authentication token used by a third
            party
        :keyword version: (VersionNumber) The version number of the caller
            OCPI module
        :keyword party_id: (CiString(3))  The requested party ID
        :keyword country_code: (CiString(2)) The requested Country code
        :keyword token_type: (TokenType) The token type
        :keyword session_id: (str) Charging profile corresponding session id.

        :return: The updated object data
        :rtype: Any
        """
        pass

    @abstractmethod
    async def delete(
        cls, module: ModuleID, role: RoleEnum, id, *args, **kwargs
    ):
        """Delete an object

        :param module: The OCPI module
        :param role: The role of the caller
        :param id: The ID of the object

        :keyword auth_token: (str) The authentication token used by a third
            party
        :keyword version: (VersionNumber) The version number of the caller
            OCPI module
        """
        pass

    @abstractmethod
    async def do(
        cls,
        module: ModuleID,
        role: Optional[RoleEnum],
        action: Action,
        *args,
        data: Optional[dict] = None,
        **kwargs,
    ) -> Any:
        """Do an action (non-CRUD)

        :param module: The OCPI module
        :param role: The role of the caller
        :param action: The action type
        :param data: The data required for the action

        :keyword auth_token: (str) The authentication token used by a third
            party
        :keyword version: (VersionNumber) The version number of the caller
            OCPI module
        :keyword response_url: (str) Response url for actions which require
            sending response.
        :keyword session: (Session) Session of charging profile action.
        :keyword duration: (int) Length of the requested ActiveChargingProfile
            in seconds.
        :keyword command: (CommandType) The command type of the OCPP command
        :keyword charging_profile (SetChargingProfile): Charging profile sent
            to be updated.

        :return: The action result
        :rtype: Any
        """
        pass
