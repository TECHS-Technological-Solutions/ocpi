import httpx
from fastapi import APIRouter, Request, WebSocket, Depends

from py_ocpi.core.adapter import Adapter
from py_ocpi.core.crud import Crud
from py_ocpi.core.schemas import Push, PushResponse, ReceiverResponse
from py_ocpi.core.utils import encode_string_base64, get_auth_token
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.config import settings
from py_ocpi.modules.versions.enums import InterfaceRole, VersionNumber


def client_url(module_id: ModuleID, object_id: str, base_url: str) -> str:
    if module_id == ModuleID.cdrs:
        return base_url
    return f'{base_url}/{settings.COUNTRY_CODE}/{settings.PARTY_ID}/{object_id}'


def client_method(module_id: ModuleID) -> str:
    if module_id == ModuleID.cdrs:
        return 'POST'
    return 'PUT'


def request_data(module_id: ModuleID, object_data: dict, adapter: Adapter) -> dict:
    data = {}
    if module_id == ModuleID.locations:
        data = adapter.location_adapter(object_data).dict()
    elif module_id == ModuleID.sessions:
        data = adapter.session_adapter(object_data).dict()
    elif module_id == ModuleID.cdrs:
        data = adapter.cdr_adapter(object_data).dict()
    elif module_id == ModuleID.tariffs:
        data = adapter.tariff_adapter(object_data).dict()
    elif module_id == ModuleID.tokens:
        data = adapter.token_adapter(object_data).dict()
    return data


async def send_push_request(
    object_id: str,
    object_data: dict,
    module_id: ModuleID,
    adapter: Adapter,
    client_auth_token: str,
    endpoints: list,
):
    data = request_data(module_id, object_data, adapter)

    base_url = ''
    for endpoint in endpoints:
        if endpoint['identifier'] == module_id and endpoint['role'] == InterfaceRole.receiver:
            base_url = endpoint['url']

    # push object to client
    async with httpx.AsyncClient() as client:
        request = client.build_request(client_method(module_id), client_url(module_id, object_id, base_url),
                                       headers={'authorization': client_auth_token}, json=data)
        response = await client.send(request)
        return response


async def push_object(version: VersionNumber, push: Push, crud: Crud, adapter: Adapter,
                      auth_token: str = None) -> PushResponse:
    receiver_responses = []
    for receiver in push.receivers:
        # get client endpoints
        client_auth_token = f'Token {encode_string_base64(receiver.auth_token)}'
        async with httpx.AsyncClient() as client:
            response = await client.get(receiver.endpoints_url,
                                        headers={'authorization': client_auth_token})
            endpoints = response.json()['data'][0]['endpoints']

        # get object data
        if push.module_id == ModuleID.tokens:
            data = await crud.get(push.module_id, RoleEnum.emsp, push.object_id,
                                  auth_token=auth_token, version=version)
        else:
            data = await crud.get(push.module_id, RoleEnum.cpo, push.object_id,
                                  auth_token=auth_token, version=version)

        response = await send_push_request(push.object_id, data, push.module_id, adapter, client_auth_token, endpoints)
        if push.module_id == ModuleID.cdrs:
            receiver_responses.append(ReceiverResponse(endpoints_url=receiver.endpoints_url,
                                                       status_code=response.status_code,
                                                       response=response.headers))
        else:
            receiver_responses.append(ReceiverResponse(endpoints_url=receiver.endpoints_url,
                                                       status_code=response.status_code,
                                                       response=response.json()))

    return PushResponse(receiver_responses=receiver_responses)


http_router = APIRouter()


# WARNING it's advised not to expose this endpoint
@http_router.post("/{version}", status_code=200, include_in_schema=False, response_model=PushResponse)
async def http_push_to_client(request: Request, version: VersionNumber, push: Push,
                              crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):
    auth_token = get_auth_token(request)

    return await push_object(version, push, crud, adapter, auth_token)


websocket_router = APIRouter()


# WARNING it's advised not to expose this endpoint
@websocket_router.websocket("/ws/{version}")
async def websocket_push_to_client(websocket: WebSocket, version: VersionNumber,
                                   crud: Crud = Depends(get_crud), adapter: Adapter = Depends(get_adapter)):

    auth_token = get_auth_token(websocket)
    await websocket.accept()

    while True:
        data = await websocket.receive_json()
        push = Push(**data)
        push_response = await push_object(version, push, crud, adapter, auth_token)
        await websocket.send_json(push_response.dict())
