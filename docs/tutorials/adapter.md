# Adapter
Adapter class has multiple adapter methods who will adapt the result from Crud to acceptable schema by OCPI.
each module in OCPI must have one or more corresponding methods in Adapter class.

The adapter methods are listed below:

- **_location_adapter_**

    - **_description_**:

        the adapter method used in Locations module

    - **_input_**:

        data: The object details

        version: The version number of the caller OCPI module

    - **_output_**: [Location](https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#131-location-object)

- **_session_adapter_**

    - **_description_**:

        the adapter method used in Sessions module

    - **_input_**:

        data: The object details

        version: The version number of the caller OCPI module

    - **_output_**: [Session](https://github.com/ocpi/ocpi/blob/2.2.1/mod_sessions.asciidoc#131-session-object)

- **_charging_preference_adapter_**

    - **_description_**:

        the adapter method used in Sessions module for charging preferences

    - **_input_**:

        data: The object details

        version: The version number of the caller OCPI module

    - **_output_**: [ChargingPreference](https://github.com/ocpi/ocpi/blob/2.2.1/mod_sessions.asciidoc#132-chargingpreferences-object)

- **_credentials_adapter_**

    - **_description_**:

        the adapter method used in Credentials module

    - **_input_**:

        data: The object details

        version: The version number of the caller OCPI module

    - **_output_**: [Credential](https://github.com/ocpi/ocpi/blob/2.2.1/credentials.asciidoc#131-credentials-object)

- **_cdr_adapter_**

    - **_description_**:

        the adapter method used in CDR module

    - **_input_**:

        data: The object details

        version: The version number of the caller OCPI module

    - **_output_**: [CDR](https://github.com/ocpi/ocpi/blob/2.2.1/mod_cdrs.asciidoc#131-cdr-object)

- **_tariff_adapter_**

    - **_description_**:

        the adapter method used in Tariffs module

    - **_input_**:

        data: The object details

        version: The version number of the caller OCPI module

    - **_output_**: [Tariff](https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#131-tariff-object)

- **_command_response_adapter_**

    - **_description_**:

        the adapter method used in Commands module for command response

    - **_input_**:

        data: The object details

        version: The version number of the caller OCPI module

    - **_output_**: [CommandResponse](https://github.com/ocpi/ocpi/blob/2.2.1/mod_commands.asciidoc#132-commandresponse-object)

- **_command_result_adapter_**

    - **_description_**:

        the adapter method used in Commands module for command result

    - **_input_**:

        data: The object details

        version: The version number of the caller OCPI module

    - **_output_**: [CommandResult](https://github.com/ocpi/ocpi/blob/2.2.1/mod_commands.asciidoc#133-commandresult-object)

- **_token_adapter_**

    - **_description_**:

        the adapter method used in Tokens module

    - **_input_**:

        data: The object details

        version: The version number of the caller OCPI module

    - **_output_**: [Token](https://github.com/ocpi/ocpi/blob/2.2.1/mod_tokens.asciidoc#132-token-object)

- **_authorization_adapter_**

    - **_description_**:

        the adapter method used in Tokens module for token authorization

    - **_input_**:

        data: The object details

        version: The version number of the caller OCPI module

    - **_output_**: [AuthorizationInfo](https://github.com/ocpi/ocpi/blob/2.2.1/mod_tokens.asciidoc#131-authorizationinfo-object)


for instance the adapter for location module is _location_adapter_ as follows.


```python
class Adapter:
    @classmethod
    def location_adapter(cls, data) -> Location:
        return Location(**data)
```