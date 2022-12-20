# Push

push is a function to send(push) object data updates to the other end of OCPI communication. push function can be called manually, or via HTTP or Websocket endpoints. in order to add push endpoints either _http\_push_ or _websocket\_push_ must be set in _get\_application_.

## Push Function
- **_input_**:

    version: The version number of the caller OCPI

    push: push request in Push schema

    crud: the CRUD class

    adapter: the Adapter class

    auth_token: The authentication token used by third party

- **_output_**: push response in PushResponse schema

## Push Endpoint

- **POST** `/{version}`

    version: The version number of the caller OCPI

    request body: push request in Push schema
