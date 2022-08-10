import uuid

import requests

from fastapi import APIRouter, Depends, HTTPException, status as fastapistatus
from pydantic import ValidationError

from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.crud import get_crud
from py_ocpi.adapter import get_adapter
from py_ocpi.core import status
from py_ocpi.core.enums import ModuleID
from py_ocpi.credentials.v_2_2_1.schemas import Credentials

router = APIRouter(
    prefix='/credentials',
)


@router.get("/", response_model=OCPIResponse)
async def get_credentials(crud=Depends(get_crud), adapter=Depends(get_adapter)):
    try:
        data_list = await crud.list(ModuleID.CredentialsAndRegistrations)
        credentials = []
        for data in data_list:
            credentials.append(adapter.credentials_adapter(data).dict())
        return OCPIResponse(
            data=credentials,
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.post("/", response_model=OCPIResponse)
async def post_credentials(credentials: Credentials, crud=Depends(get_crud), adapter=Depends(get_adapter)):
    try:
        # Check if the client is already registered
        credentials_client_token = credentials.token
        server_cred = crud.get(ModuleID.CredentialsAndRegistrations, credentials.token)
        if server_cred:
            raise HTTPException(fastapistatus.HTTP_405_METHOD_NOT_ALLOWED, "Client has been already registered")

        # Retrieve the versions and endpoints from the client
        response_versions = requests.get(credentials.url, auth=credentials_client_token)
        response_endpoints = requests.get(response_versions.json()['data']['url'], auth=credentials_client_token)

        # Generate new credentials token
        if response_endpoints.status_code == fastapistatus.HTTP_200_OK:
            cred_token_c = uuid.uuid4()
            new_credentials = crud.update(server_cred, {'token': cred_token_c})
            return OCPIResponse(
                data=[adapter.credentials_adapter(new_credentials).dict()],
                **status.OCPI_1000_GENERIC_SUCESS_CODE
            )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )


@router.put("/", response_model=OCPIResponse)
async def update_credentials(credentials: Credentials, crud=Depends(get_crud), adapter=Depends(get_adapter)):
    try:
        # Check if the client is already registered
        credentials_client_token = credentials.token
        server_cred = crud.get(ModuleID.CredentialsAndRegistrations, credentials.token)
        if not server_cred:
            raise HTTPException(fastapistatus.HTTP_405_METHOD_NOT_ALLOWED, "Client has not been already registered")

        # Switch to the version that contains clients credentials
        response_server_version = requests.get(server_cred.url, auth=server_cred.token)
        server_versions = response_server_version.json()['data']['version']
        response_client_versions = requests.get(credentials.url, auth=credentials_client_token)
        client_version = response_client_versions.json()['data']['version']
        if not server_versions == client_version:
            server_cred = crud.update(server_cred, {'url': credentials.url})

        # Fetch client endpoints
        response_endpoints = requests.get(response_client_versions.json()['data']['url'], auth=credentials_client_token)

        # Generate new credentials token
        if response_endpoints.status_code == fastapistatus.HTTP_200_OK:
            cred_token_c = uuid.uuid4()
            new_credentials = crud.update(server_cred, {'token': cred_token_c})
            return OCPIResponse(
                data=[adapter.credentials_adapter(new_credentials).dict()],
                **status.OCPI_1000_GENERIC_SUCESS_CODE
            )

    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )
