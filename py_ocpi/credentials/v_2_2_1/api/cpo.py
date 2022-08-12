import uuid
import httpx

from fastapi import APIRouter, Depends, HTTPException, status as fastapistatus
from pydantic import ValidationError

from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.crud import get_crud
from py_ocpi.adapter import get_adapter
from py_ocpi.core import status
from py_ocpi.core.enums import ModuleID
from py_ocpi.credentials.v_2_2_1.schemas import Credentials, ServerCredentials

router = APIRouter(
    prefix='/credentials',
)


@router.get("/", response_model=OCPIResponse)
async def get_credentials(crud=Depends(get_crud), adapter=Depends(get_adapter)):
    try:
        data = await crud.get(ModuleID.CredentialsAndRegistrations)
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
        server_cred = await crud.get(ServerCredentials, credentials_client_token)
        if server_cred:
            raise HTTPException(fastapistatus.HTTP_405_METHOD_NOT_ALLOWED, "Client is already registered")

        # Retrieve the versions and endpoints from the client
        async with httpx.AsyncClient() as client:
            response_versions = await client.get(credentials.url, headers=credentials_client_token)
            versions = response_versions.json()['data'][0]
            response_endpoints = await client.get(versions['url'], headers=credentials_client_token)

        if response_endpoints.status_code == fastapistatus.HTTP_200_OK:

            # Store client credentials
            # TODO: Think of passing url and business details of server
            #  because in respond client should get the server details
            endpoints = response_endpoints.json()['data'][0]
            server_cred = await crud.create(ServerCredentials(
                cred_token_b=credentials.token,
                versions=versions,
                endpoints=endpoints
            ))

            # Generate new credentials for sender
            new_credentials = await crud.create(Credentials(
                token=uuid.uuid4(),
                url=server_cred.url,
                roles=server_cred.roles
            ))
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
        server_cred = await crud.get(ServerCredentials, credentials_client_token)
        if not server_cred:
            raise HTTPException(fastapistatus.HTTP_405_METHOD_NOT_ALLOWED, "Client is not registered")

        # Retrieve the versions and endpoints from the client
        async with httpx.AsyncClient() as client:
            response_versions = await client.get(credentials.url, headers=credentials_client_token)
            versions = response_versions.json()['data'][0]
            response_endpoints = await client.get(versions['url'], headers=credentials_client_token)

        if response_endpoints.status_code == fastapistatus.HTTP_200_OK:

            # Update server credentials to access client's system
            endpoints = response_endpoints.json()['data'][0]
            server_cred = await crud.update(server_cred, {'versions': versions, 'endpoints': endpoints})

            # Generate new credentials token
            cred_token_c = uuid.uuid4()
            new_credentials = await crud.create(Credentials(
                token=cred_token_c,
                url=server_cred.url,
                roles=server_cred.roles
            ))
            return OCPIResponse(
                data=[adapter.credentials_adapter(new_credentials).dict()],
                **status.OCPI_1000_GENERIC_SUCESS_CODE
            )

    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )
