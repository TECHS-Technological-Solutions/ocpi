# CRUD
The CRUD class is responsible of getting the required info for proper OCPI communication. for each OCPI API call, the corresponding method from Crud class will be called.

The CRUD methods are listed below:

- **_get_**

    - **_description_**:

        used for getting a data object

    - **_input_**:

        module: The OCPI module

        role: The role of the caller

        id: The ID of the object

        auth_token: The authentication token used by third party

        version: The version number of the caller OCPI module

        party_id: The requested party ID

        country_code: The requested Country code

        token_type: The token type

        command: The command type of the OCPP command

        > **_NOTE:_** party_id, country_code, token_type, command are only present when a module pass them

    - **_output_**: the object data in dict

- **_list_**

    - **_description_**:

        used for getting the list of data objects

    - **_input_**:

        module: The OCPI module

        role: The role of the caller

        filters: [OCPI pagination filters](https://github.com/ocpi/ocpi/blob/master/transport_and_format.asciidoc#paginated-request)

        auth_token: The authentication token used by third party

        version: The version number of the caller OCPI module

        party_id: The requested party ID

        country_code: The requested Country code

        > **_NOTE:_** party_id and country_code are only present when a module pass them

    - **_output_**: a tuple containing Objects list, Total number of objects and if it's the last page or not(for pagination) (list, int, bool)

- **_create_**

    - **_description_**:

        used for creating a data object

    - **_input_**:

        module: The OCPI module

        role: The role of the caller

        data: The object details

        auth_token: The authentication token used by third party

        version: The version number of the caller OCPI module

        party_id: The requested party ID

        country_code: The requested Country code

        token_type: The token type

        command: The command type (used in Commands module)

        operation : The operation type in credentials and registration process the value is either 'credentials' or 'registration'

        > **_NOTE:_** party_id, country_code and token_type are only present when a module pass them

    - **_output_**: the newly created object data in dict

- **_update_**

    - **_description_**:

        used for updating a data object

    - **_input_**:

        module: The OCPI module

        role: The role of the caller

        data: The object details

        id: The ID of the object

        auth_token: The authentication token used by third party

        version: The version number of the caller OCPI module

        party_id: The requested party ID

        country_code: The requested Country code

        token_type: The token type

        operation : The operation type in credentials and registration process the value is either 'credentials' or 'registration'

    - **_output_**: the updated object data in dict

- **_delete_**

    - **_description_**:

        used for deleting a data object

    - **_input_**:

        module: The OCPI module

        role: The role of the caller

        id: The ID of the object

        auth_token: The authentication token used by third party

        version: The version number of the caller OCPI module

    - **_output_**: None

- **_do_**

    - **_description_**:

        used for doing an action or a non-CRUD operation

    - **_input_**:

        module: The OCPI module

        role: The role of the caller

        action: The action type. it can be either 'SendCommand', 'GetClientToken' or 'AuthorizeToken'

        data: The data required for the action

        command: The command type of the OCPP command

        auth_token: The authentication token used by third party

        version: The version number of the caller OCPI module

    - **_output_**: The action result in dict
