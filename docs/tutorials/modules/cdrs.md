# CDRs

Every CRUD method call from this module has _module\_id_ = cdrs, _auth\_token_ = {token used in HTTP request header}, version = {OCPI version of the module}

## CPO
Every CRUD method call from this module has _role_ = CPO

- **GET** `/`

    crud.list is called with _filters_ argument containing _date\_from_, _date\_to_, _offset_ and _limit_ keys

## EMSP
Every CRUD method call from this module has _role_ = EMSP

- **GET** `/{cdr_id}`

    crud.get is called with _id_ = _cdr\_id_

- **PUT** `/`

    crud.create is called with data = dict (with standard OCPI CDR schema)
