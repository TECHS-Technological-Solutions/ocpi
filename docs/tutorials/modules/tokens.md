# Tokens

Every CRUD method call from this module has _module\_id_ = tokens, _auth\_token_ = {token used in HTTP request header}, version = {OCPI version of the module}

## CPO
Every CRUD method call from this module has _role_ = CPO

- **GET** `/{country_code}/{party_id}/{token_uid}`

    crud.get is called with _id_ = _token\_uid_, _country\_code_ = _country\_code_, _party\_id_ = _party\_id_ and _token\_type_ = (_token\_type_ passed in query parameters)

- **PUT** `/{country_code}/{party_id}/{token_uid}`

    crud.get is called with _id_ = _token\_uid_, _country\_code_ = _country\_code_, _party\_id_ = _party\_id_ and _token\_type_ = (_token\_type_ passed in query parameters)

    if object exists crud.update is called with _id_ = _token\_uid_, data = dict (with standard OCPI Token schema), _country\_code_ = _country\_code_, _party\_id_ = _party\_id_ and _token\_type_ = (_token\_type_ passed in query parameters)

    if object doesn't exist crud.create is called with data = dict (with standard OCPI Token schema), _country\_code_ = _country\_code_, _party\_id_ = _party\_id_ and _token\_type_ = (_token\_type_ passed in query parameters)

- **PATCH** `/{country_code}/{party_id}/{token_uid}`

    crud.get is called with _id_ = _token\_uid_, _country\_code_ = _country\_code_, _party\_id_ = _party\_id_ and _token\_type_ = (_token\_type_ passed in query parameters)

    crud.update is called with _id_ = _token\_uid_, data = dict (with standard OCPI Token schema), _country\_code_ = _country\_code_, _party\_id_ = _party\_id_ and _token\_type_ = (_token\_type_ passed in query parameters)

## EMSP
Every CRUD method call from this module has _role_ = EMSP

- **GET** `/`

    crud.list is called with _filters_ argument containing _date\_from_, _date\_to_, _offset_ and _limit_ keys

- **POST** `/{token_uid}/authorize`

    crud.get is called with _id_ = _token\_uid_ and _token\_type_ = (_token\_type_ passed in query parameters)

    crud.do is called with _action_ = 'AuthorizeToken',  _data_ = dict (with keys 'token_uid': _token\_uid_, 'token_type': _token\_type_, 'location_reference': request body with standard OCPI LocationReference schema),
