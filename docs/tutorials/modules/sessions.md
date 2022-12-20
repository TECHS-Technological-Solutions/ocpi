# Sessions

Every CRUD method call from this module has _module\_id_ = sessions, _auth\_token_ = {token used in HTTP request header}, version = {OCPI version of the module}

## CPO
Every CRUD method call from this module has _role_ = CPO

- **GET** `/`

    crud.list is called with _filters_ argument containing _date\_from_, _date\_to_, _offset_ and _limit_ keys

- **PUT** `/{session_id}/charging_preferences`

    crud.update is called with _id_ = _session\_id_ and data = dict (with standard OCPI Charging Preference schema)

## EMSP
Every CRUD method call from this module has _role_ = EMSP

- **GET** `/{country_code}/{party_id}/{session_id}`

    crud.get is called with _id_ = _session\_id_, _country\_code_ = _country\_code_ and _party\_id_ = _party\_id_

- **PUT** `/{country_code}/{party_id}/{session_id}`

    crud.get is called with _id_ = _session\_id_, _country\_code_ = _country\_code_ and _party\_id_ = _party\_id_

    if object exists crud.update is called with _id_ = _session\_id_, data = dict (with standard OCPI Session schema), _country\_code_ = _country\_code_ and _party\_id_ = _party\_id_

    if object doesn't exist crud.create is called with data = dict (with standard OCPI Session schema), _country\_code_ = _country\_code_ and _party\_id_ = _party\_id_

- **PATCH** `/{country_code}/{party_id}/{session_id}`

    crud.get is called with _id_ = _session\_id_, _country\_code_ = _country\_code_ and _party\_id_ = _party\_id_

    crud.update is called with _id_ = _session\_id_, data = dict (with standard OCPI Session schema), _country\_code_ = _country\_code_ and _party\_id_ = _party\_id_
