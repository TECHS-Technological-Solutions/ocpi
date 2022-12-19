# Credentials

Every CRUD method call from this module has _module\_id_ = credentials, _auth\_token_ = {token used in HTTP request header}, version = {OCPI version of the module}

## CPO
Every CRUD method call from this module has _role_ = CPO

- **GET** `/`

    crud.get is called with _id_ = {token used in HTTP request header}

- **post** `/`

    crud.do is called with _action_ = 'GetClientToken' and _module\_id_ = credentials

    crud.create is called with data = dict (with keys 'credentials': the request body with OCPI Credentials schema and 'endpoints': the response from client version details)

- **put** `/`

    crud.do is called with _action_ = 'GetClientToken' and _module\_id_ = credentials

    crud.update is called with data = dict (with keys 'credentials': the request body with OCPI Credentials schema and 'endpoints': the response from client version details)

## EMSP
Every CRUD method call from this module has _role_ = EMSP

- **GET** `/`

    crud.get is called with _id_ = {token used in HTTP request header}

- **post** `/`

    crud.do is called with _action_ = 'GetClientToken' and _module\_id_ = credentials

    crud.create is called with data = dict (with keys 'credentials': the request body with OCPI Credentials schema and 'endpoints': the response from client version details)

- **put** `/`

    crud.do is called with _action_ = 'GetClientToken' and _module\_id_ = credentials

    crud.update is called with data = dict (with keys 'credentials': the request body with OCPI Credentials schema and 'endpoints': the response from client version details)
