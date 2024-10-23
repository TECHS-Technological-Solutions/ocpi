from typing import Union

import httpx
from fastapi import APIRouter, Request, WebSocket, Depends

from py_ocpi.core.adapter import Adapter
from py_ocpi.core.authentication.verifier import (
    HttpPushVerifier,
    WSPushVerifier,
)
from py_ocpi.core.crud import Crud
from py_ocpi.core.schemas import Push, PushResponse, ReceiverResponse
from py_ocpi.core.utils import encode_string_base64, get_auth_token
from py_ocpi.core.dependencies import get_crud, get_adapter
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.config import settings, logger
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.versions.v_2_2_1.enums import InterfaceRole


def client_url(module_id: ModuleID, object_id: str, base_url: str) -> str:
    if module_id == ModuleID.cdrs:
        return base_url
    return f"{base_url}{settings.COUNTRY_CODE}/{settings.PARTY_ID}/{object_id}"


def client_method(module_id: ModuleID) -> str:
    if module_id == ModuleID.cdrs:
        return "POST"
    return "PUT"


def request_data(
    module_id: ModuleID,
    object_data: dict,
    adapter: Adapter,
    version: VersionNumber,
) -> dict:
    data = {}
    if module_id == ModuleID.locations:
        data = adapter.location_adapter(object_data, version).dict()
    elif module_id == ModuleID.sessions:
        data = adapter.session_adapter(object_data, version).dict()
    elif module_id == ModuleID.cdrs:
        data = adapter.cdr_adapter(object_data, version).dict()
    elif module_id == ModuleID.tariffs:
        data = adapter.tariff_adapter(object_data, version).dict()
    elif module_id == ModuleID.tokens:
        data = adapter.token_adapter(object_data, version).dict()
    return data


async def send_push_request(
    object_id: str,
    object_data: dict,
    module_id: ModuleID,
    adapter: Adapter,
    client_auth_token: str,
    endpoints: list,
    version: VersionNumber,
):
    data = request_data(module_id, object_data, adapter, version)

    base_url = ""
    for endpoint in endpoints:
        if (
            version.value.startswith("2.2")
            and endpoint["identifier"] == module_id
            and endpoint["role"] == InterfaceRole.receiver
        ) or (
            version.value.startswith("2.1")
            and endpoint["identifier"] == module_id
        ):
            base_url = endpoint["url"]

    # push object to client
    async with httpx.AsyncClient() as client:
        request = client.build_request(
            client_method(module_id),
            client_url(module_id, object_id, base_url),
            headers={"Authorization": client_auth_token},
            json=data,
        )
        response = await client.send(request)
        return response


async def push_object(
    version: VersionNumber,
    push: Push,
    crud: Crud,
    adapter: Adapter,
    auth_token: Union[str, None] = None,
) -> PushResponse:
    receiver_responses = []
    for receiver in push.receivers:
        # get client endpoints
        if version.value.startswith("2.1") or version.value.startswith("2.0"):
            token = receiver.auth_token
        else:
            token = encode_string_base64(receiver.auth_token)

        client_auth_token = f"Token {token}"

        async with httpx.AsyncClient() as client:
            logger.info(
                "Send request to get version details: %s"
                % receiver.endpoints_url
            )
            response = await client.get(
                receiver.endpoints_url,
                headers={"authorization": client_auth_token},
            )
            logger.info("Response status_code - `%s`" % response.status_code)
            endpoints = response.json()["data"]["endpoints"]
            logger.debug("Endpoints response data - `%s`" % endpoints)

        # get object data
        if push.module_id == ModuleID.tokens:
            logger.debug("Requested module with push is token.")
            data = await crud.get(
                push.module_id,
                RoleEnum.emsp,
                push.object_id,
                auth_token=auth_token,
                version=version,
            )
        else:
            logger.debug("Requested module with push is `%s`." % push.module_id)
            data = await crud.get(
                push.module_id,
                RoleEnum.cpo,
                push.object_id,
                auth_token=auth_token,
                version=version,
            )

        response = await send_push_request(
            push.object_id,
            data,
            push.module_id,
            adapter,
            client_auth_token,
            endpoints,
            version,
        )
        if push.module_id == ModuleID.cdrs:
            logger.debug("Add headers for CDR module into response.")
            receiver_responses.append(
                ReceiverResponse(
                    endpoints_url=receiver.endpoints_url,
                    status_code=response.status_code,
                    response=response.headers,
                )
            )
        else:
            receiver_responses.append(
                ReceiverResponse(
                    endpoints_url=receiver.endpoints_url,
                    status_code=response.status_code,
                    response=response.json(),
                )
            )
    result = PushResponse(receiver_responses=receiver_responses)
    logger.debug("Result of push operation - %s" % result.dict())
    return result


http_router = APIRouter(
    dependencies=[Depends(HttpPushVerifier())],
)


# WARNING it's advised not to expose this endpoint
@http_router.post(
    "/{version}",
    status_code=200,
    include_in_schema=False,
    response_model=PushResponse,
)
async def http_push_to_client(
    request: Request,
    version: VersionNumber,
    push: Push,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    logger.info("Received push http request.")
    logger.debug("Received push data - `%s`" % push.dict())
    auth_token = get_auth_token(request, version)

    return await push_object(version, push, crud, adapter, auth_token)


websocket_router = APIRouter(
    dependencies=[Depends(WSPushVerifier())],
)


# WARNING it's advised not to expose this endpoint
@websocket_router.websocket("/ws/{version}")
async def websocket_push_to_client(
    websocket: WebSocket,
    version: VersionNumber,
    crud: Crud = Depends(get_crud),
    adapter: Adapter = Depends(get_adapter),
):
    auth_token = get_auth_token(websocket, version)
    await websocket.accept()

    while True:
        data = await websocket.receive_json()
        logger.debug("Received data through ws - `%s`" % data)
        push = Push(**data)
        push_response = await push_object(
            version, push, crud, adapter, auth_token
        )
        logger.debug("Sending push response - `%s`" % push_response.dict())
        await websocket.send_json(push_response.dict())
