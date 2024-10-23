from abc import ABC, abstractmethod

from py_ocpi.core.utils import get_module_model
from py_ocpi.modules.versions.enums import VersionNumber


class Adapter(ABC):
    @abstractmethod
    def location_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Location schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            Location: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def session_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Session schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            Session: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def charging_preference_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI ChargingPreference schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            ChargingPreference: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def credentials_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Credential schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            Credential: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def cdr_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI CDR schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            CDR: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def tariff_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Tariff schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            Tariff: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def command_response_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI CommandResponse schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            CommandResponse: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def command_result_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI CommandResult schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            CommandResult: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def token_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Token schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            Token: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def authorization_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI AuthorizationInfo schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            AuthorizationInfo: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def hubclientinfo_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI ClientInfo schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            ClientInfo: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def charging_profile_response_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI ChargingProfileResponse schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            ChargingProfileResponse: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def active_charging_profile_result_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI ActiveChargingProfileResult schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module


            ActiveChargingProfileResult: The object data in proper OCPI schema
        """
        pass

    @abstractmethod
    def clear_profile_result_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI ClearProfileResult schema

        Args:
            data (dict): The object details
            version (VersionNumber, optional):
            The version number of the caller OCPI module

        Returns:
            ClearProfileResult: The object data in proper OCPI schema
        """
        pass


class BaseAdapter(Adapter):
    @classmethod
    def location_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Location schema"""
        return get_module_model(
            class_name="Location",
            module_name="locations",
            version_name=version.name,
        )(**data)

    @classmethod
    def session_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Session schema"""
        return get_module_model(
            class_name="Session",
            module_name="sessions",
            version_name=version.name,
        )(**data)

    @classmethod
    def charging_preference_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI ChargingPreference schema"""
        return get_module_model(
            class_name="ChargingPreferences",
            module_name="sessions",
            version_name=version.name,
        )(**data)

    @classmethod
    def credentials_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Credentials schema"""
        return get_module_model(
            class_name="Credentials",
            module_name="credentials",
            version_name=version.name,
        )(**data)

    @classmethod
    def cdr_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Cdr schema"""
        return get_module_model(
            class_name="Cdr",
            module_name="cdrs",
            version_name=version.name,
        )(**data)

    @classmethod
    def tariff_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Tariff schema"""
        return get_module_model(
            class_name="Tariff",
            module_name="tariffs",
            version_name=version.name,
        )(**data)

    @classmethod
    def command_response_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI CommandResponse schema"""
        return get_module_model(
            class_name="CommandResponse",
            module_name="commands",
            version_name=version.name,
        )(**data)

    @classmethod
    def command_result_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI CommandResult schema"""
        return get_module_model(
            class_name="CommandResult",
            module_name="commands",
            version_name=version.name,
        )(**data)

    @classmethod
    def token_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI Token schema"""
        return get_module_model(
            class_name="Token",
            module_name="tokens",
            version_name=version.name,
        )(**data)

    @classmethod
    def authorization_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI AuthorizationInfo schema"""
        return get_module_model(
            class_name="AuthorizationInfo",
            module_name="tokens",
            version_name=version.name,
        )(**data)

    @classmethod
    def hubclientinfo_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI ClientInfo schema"""
        return get_module_model(
            class_name="ClientInfo",
            module_name="hubclientinfo",
            version_name=version.name,
        )(**data)

    @classmethod
    def charging_profile_response_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI ChargingProfileResponse schema"""
        return get_module_model(
            class_name="ChargingProfileResponse",
            module_name="chargingprofiles",
            version_name=version.name,
        )(**data)

    @classmethod
    def active_charging_profile_result_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI ActiveChargingProfileResult schema"""
        return get_module_model(
            class_name="ActiveChargingProfileResult",
            module_name="chargingprofiles",
            version_name=version.name,
        )(**data)

    @classmethod
    def clear_profile_result_adapter(
        cls, data: dict, version: VersionNumber = VersionNumber.latest
    ):
        """Adapt the data to OCPI ClearProfileResult schema"""
        return get_module_model(
            class_name="ClearProfileResult",
            module_name="chargingprofiles",
            version_name=version.name,
        )(**data)
