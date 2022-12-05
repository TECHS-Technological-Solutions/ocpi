import httpx
from fastapi import APIRouter, Request, Depends

from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core.schemas import Push, PushResponse, ReceiverResponse
from py_ocpi.core.utils import get_auth_token
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.config import settings
from py_ocpi.modules.versions.enums import InterfaceRole, VersionNumber

router = APIRouter(
)


async def push_object(
    object_id: str,
    object_data: dict,
    module_id: ModuleID,
    adapter: Adapter,
    emsp_auth_token: str,
    endpoints: list,
):
    push_data = {}
    if module_id == ModuleID.locations:
        push_data = adapter.location_adapter(object_data).dict()
    elif module_id == ModuleID.sessions:
        push_data = adapter.session_adapter(object_data).dict()

    push_url = ''
    for endpoint in endpoints:
        if endpoint['identifier'] == module_id and endpoint['role'] == InterfaceRole.receiver:
            push_url = endpoint['url']

    # push object to emsp
    async with httpx.AsyncClient() as client:
        response = await client.put(f'{push_url}/{settings.COUNTRY_CODE}/{settings.PARTY_ID}/{object_id}',
                                    headers={'authorization': emsp_auth_token}, json=push_data)
        return response


# WARNING it's advised not to expose this endpoint
@router.get("/{version}", status_code=200, include_in_schema=False, response_model=PushResponse)
async def push_to_emsp(request: Request, version: VersionNumber, push: Push,
                       crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
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
        response = await push_object(push.object_id, data, push.module_id, adapter, emsp_auth_token, endpoints)
        receiver_responses.append(ReceiverResponse(receiver.endpoints_url, status_code=response.status_code,
                                                   response=response.json()))

    return PushResponse(receiver_responses=receiver_responses)
