import httpx

from fastapi import APIRouter, Depends, HTTPException, Request, status as fastapistatus
from pydantic import ValidationError

from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.utils import get_auth_token
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core import status
from py_ocpi.core.enums import ModuleID
from py_ocpi.credentials.v_2_2_1.schemas import Credentials, ServerCredentials

router = APIRouter(
    prefix='/credentials',
)


@router.get("/", response_model=OCPIResponse)
async def get_credentials(request: Request, crud=Depends(get_crud), adapter=Depends(get_adapter)):
    token = get_auth_token(request)
    try:
        data = await crud.get(ModuleID.credentials_and_registration, token)
        return OCPIResponse(
            data=[adapter.credentials_adapter(data).dict()],
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
        server_cred = await crud.get(ModuleID.credentials_and_registration, credentials_client_token)
        if server_cred:
            raise HTTPException(fastapistatus.HTTP_405_METHOD_NOT_ALLOWED, "Client is already registered")

        # Retrieve the versions and endpoints from the client
        async with httpx.AsyncClient() as client:
            authorization_token = f'Token {credentials_client_token}'
            response_versions = await client.get(credentials.url,
                                                 headers={'authorization': authorization_token})
            versions = response_versions.json()['data'][0]
            response_endpoints = await client.get(versions['url'],
                                                  headers={'authorization': authorization_token})

        if response_endpoints.status_code == fastapistatus.HTTP_200_OK:

            # Store client credentials
            endpoints = response_endpoints.json()['data'][0]
            await crud.create(ModuleID.credentials_and_registration, ServerCredentials(
                cred_token_b=credentials.token,
                versions=versions,
                endpoints=endpoints
            ))

            # Generate new credentials for sender
            new_credentials = await crud.create(ModuleID.credentials_and_registration, {'url': versions['url']})
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
        server_cred = await crud.get(ModuleID.credentials_and_registration, credentials_client_token)
        if not server_cred:
            raise HTTPException(fastapistatus.HTTP_405_METHOD_NOT_ALLOWED, "Client is not registered")

        # Retrieve the versions and endpoints from the client
        async with httpx.AsyncClient() as client:
            authorization_token = f'Token {credentials_client_token}'
            response_versions = await client.get(credentials.url, headers={'authorization': authorization_token})
            versions = response_versions.json()['data'][0]
            response_endpoints = await client.get(versions['url'], headers={'authorization': authorization_token})

        if response_endpoints.status_code == fastapistatus.HTTP_200_OK:

            # Update server credentials to access client's system
            endpoints = response_endpoints.json()['data'][0]
            await crud.update(ModuleID.credentials_and_registration,
                              ServerCredentials(cred_token_b=credentials.token,
                                                versions=versions,
                                                endpoints=endpoints),
                              server_cred.cred_token_b)

            # Generate new credentials token
            new_credentials = await crud.create(ModuleID.credentials_and_registration, {'url': versions['url']})
            return OCPIResponse(
                data=[adapter.credentials_adapter(new_credentials).dict()],
                **status.OCPI_1000_GENERIC_SUCESS_CODE
            )

    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )
