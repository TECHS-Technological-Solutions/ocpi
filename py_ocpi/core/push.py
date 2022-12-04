import httpx
from fastapi import APIRouter, Request, Depends

from py_ocpi.core.adapter import Adapter
from py_ocpi.core.schemas import Push, PushResponse, ReceiverResponse
from py_ocpi.core.utils import get_auth_token
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.config import settings
from py_ocpi.modules.versions.enums import InterfaceRole, VersionNumber

router = APIRouter(
)


async def push_location(
    location_id: str,
    location_data: dict,
    adapter: Adapter,
    emsp_auth_token: str,
    endpoints: list,
):
    push_data = adapter.location_adapter(location_data).dict()
    push_url = ''
    for endpoint in endpoints:
        if endpoint['identifier'] == ModuleID.locations and endpoint['role'] == InterfaceRole.receiver:
            push_url = endpoint['url']

    # push location to emsp
    async with httpx.AsyncClient() as client:
        response = await client.put(f'{push_url}/{settings.COUNTRY_CODE}/{settings.PARTY_ID}/{location_id}',
                                    headers={'authorization': emsp_auth_token}, json=push_data)
        return response


# WARNING it's advised not to expose this endpoint
@router.get("/{version}", status_code=200, include_in_schema=False, response_model=PushResponse)
async def push_object(request: Request, version: VersionNumber, push: Push,
                      crud=Depends(get_crud), adapter=Depends(get_adapter)):
    auth_token = get_auth_token(request)

    receiver_responses = []
    for receiver in push.receivers:
        # get emsp endpoints
        emsp_auth_token = f'Token {receiver.auth_token}'
        async with httpx.AsyncClient() as client:
            response = await client.get(receiver.endpoints_url,
                                        headers={'authorization': emsp_auth_token})
            endpoints = response.json()['data'][0]['endpoints']

        # get object data
        data = await crud.get(push.module_id, RoleEnum.cpo, push.object_id, auth_token=auth_token, version=version)
        if push.module_id == ModuleID.locations:
            response = await push_location(push.object_id, data, adapter, emsp_auth_token, endpoints)
            receiver_responses.append(ReceiverResponse(receiver.endpoints_url, status_code=response.status_code,
                                                       response=response.json()))

    return PushResponse(receiver_responses=receiver_responses)
