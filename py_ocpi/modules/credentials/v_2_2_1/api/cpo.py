import httpx

from fastapi import APIRouter, Depends, HTTPException, Request, status as fastapistatus

from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core.utils import encode_string_base64, get_auth_token
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core import status
from py_ocpi.core.enums import Action, ModuleID, RoleEnum
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.credentials.v_2_2_1.schemas import Credentials

router = APIRouter(
    prefix='/credentials',
)


@router.get("/", response_model=OCPIResponse)
async def get_credentials(request: Request, crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    data = await crud.get(ModuleID.credentials_and_registration, RoleEnum.cpo,
                          auth_token, auth_token=auth_token, version=VersionNumber.v_2_2_1)
    return OCPIResponse(
        data=adapter.credentials_adapter(data).dict(),
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )


@router.post("/", response_model=OCPIResponse)
async def post_credentials(request: Request, credentials: Credentials,
                           crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    # Check if the client is already registered
    credentials_client_token = credentials.token
    server_cred = await crud.do(ModuleID.credentials_and_registration, RoleEnum.cpo, Action.get_client_token,
                                version=VersionNumber.v_2_2_1, auth_token=auth_token)
    if server_cred:
        raise HTTPException(fastapistatus.HTTP_405_METHOD_NOT_ALLOWED, "Client is already registered")

    # Retrieve the versions and endpoints from the client
    async with httpx.AsyncClient() as client:
        authorization_token = f'Token {encode_string_base64(credentials_client_token)}'
        response_versions = await client.get(credentials.url,
                                             headers={'authorization': authorization_token})

        if response_versions.status_code == fastapistatus.HTTP_200_OK:
            version_url = None
            versions = response_versions.json()['data']

            for version in versions:
                if version['version'] == VersionNumber.v_2_2_1:
                    version_url = version['url']

            if not version_url:
                return OCPIResponse(
                    data=[],
                    **status.OCPI_3002_UNSUPPORTED_VERSION,
                )

            response_endpoints = await client.get(version_url,
                                                  headers={'authorization': authorization_token})

            if response_endpoints.status_code == fastapistatus.HTTP_200_OK:
                # Store client credentials and generate new credentials for sender
                endpoints = response_endpoints.json()['data']
                new_credentials = await crud.create(
                    ModuleID.credentials_and_registration, RoleEnum.cpo,
                    {
                        "credentials": credentials.dict(),
                        "endpoints": endpoints
                    },
                    auth_token=auth_token,
                    version=VersionNumber.v_2_2_1
                )

                return OCPIResponse(
                    data=adapter.credentials_adapter(new_credentials).dict(),
                    **status.OCPI_1000_GENERIC_SUCESS_CODE
                )

    return OCPIResponse(
        data=[],
        **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
    )


@router.put("/", response_model=OCPIResponse)
async def update_credentials(request: Request, credentials: Credentials,
                             crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    # Check if the client is already registered
    credentials_client_token = credentials.token
    server_cred = await crud.do(ModuleID.credentials_and_registration, RoleEnum.cpo, Action.get_client_token,
                                version=VersionNumber.v_2_2_1, auth_token=auth_token)
    if not server_cred:
        raise HTTPException(fastapistatus.HTTP_405_METHOD_NOT_ALLOWED, "Client is not registered")

    # Retrieve the versions and endpoints from the client
    async with httpx.AsyncClient() as client:
        authorization_token = f'Token {encode_string_base64(credentials_client_token)}'
        response_versions = await client.get(credentials.url, headers={'authorization': authorization_token})

        if response_versions.status_code == fastapistatus.HTTP_200_OK:
            version_url = None
            versions = response_versions.json()['data']

            for version in versions:
                if version['version'] == VersionNumber.v_2_2_1:
                    version_url = version['url']

            if not version_url:
                return OCPIResponse(
                    data=[],
                    **status.OCPI_3002_UNSUPPORTED_VERSION,
                )

            response_endpoints = await client.get(version_url,
                                                  headers={'authorization': authorization_token})

            if response_endpoints.status_code == fastapistatus.HTTP_200_OK:
                # Update server credentials to access client's system and generate new credentials token
                endpoints = response_endpoints.json()['data']
                new_credentials = await crud.update(ModuleID.credentials_and_registration, RoleEnum.cpo,
                                                    {
                                                        "credentials": credentials.dict(),
                                                        "endpoints": endpoints
                                                    },
                                                    auth_token=auth_token,
                                                    version=VersionNumber.v_2_2_1)

                return OCPIResponse(
                    data=adapter.credentials_adapter(new_credentials).dict(),
                    **status.OCPI_1000_GENERIC_SUCESS_CODE
                )

    return OCPIResponse(
        data=[],
        **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
    )


@router.delete("/", response_model=OCPIResponse)
async def remove_credentials(request: Request, crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    data = await crud.get(ModuleID.credentials_and_registration, RoleEnum.cpo,
                          auth_token, auth_token=auth_token, version=VersionNumber.v_2_2_1)
    if not data:
        raise HTTPException(fastapistatus.HTTP_405_METHOD_NOT_ALLOWED, "Client is not registered")

    await crud.delete(ModuleID.credentials_and_registration, RoleEnum.cpo,
                      auth_token, auth_token=auth_token, version=VersionNumber.v_2_2_1)

    return OCPIResponse(
        data=[],
        **status.OCPI_1000_GENERIC_SUCESS_CODE,
    )
