# Commands

Every CRUD method call from this module has _auth\_token_ = {token used in HTTP request header}, version = {OCPI version of the module}

## CPO
Every CRUD method call from this module has _role_ = CPO

- **POST** `/{command_type}`

    if _location\_id_ is present in request body crud.get is called with _module\_id_ = locations and _id_ = _location\_id_

    crud.do is called with _action_ = 'SendCommand',  _data_ = dict (with standard OCPI Command schema based on command type), _command_ = _command\_type_ and _module\_id_ = commands

    crud.do is called with _action_ = 'GetClientToken' and _module\_id_ = commands

    crud.get is called every 2s for 5min to get command result with _command_ = _command\_type_ and _id_ = 0 (ignore _id_)

## EMSP
Every CRUD method call from this module has _role_ = EMSP

- **POST** `/{uid}`

    crud.update is called with _module\_id_ = commands, _data_ = dict (with standard OCPI CommandResult schema) and _id_ = _uid_
