import urllib
import base64

from fastapi import Response, Request
from pydantic import BaseModel

from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.config import settings
from py_ocpi.modules.versions.enums import VersionNumber


def set_pagination_headers(response: Response, link: str, total: int, limit: int):
    response.headers['Link'] = link
    response.headers['X-Total-Count'] = str(total)
    response.headers['X-Limit'] = str(limit)
    return response


def get_auth_token(request: Request) -> str:
    headers = request.headers
    headers_token = headers.get('authorization', 'Token Null')
    return headers_token.split()[1]


async def get_list(response: Response, filters: dict, module: ModuleID, role: RoleEnum,
                   version: VersionNumber, crud, *args, **kwargs):
    data_list, total, is_last_page = await crud.list(module, role, filters, *args, version=version, **kwargs)

    link = ''
    params = dict(**filters)
    params['offset'] = filters['offset'] + filters['limit']
    if not is_last_page:
        link = (f'<https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                f'/{version}/{module}/?{urllib.parse.urlencode(params)}>; rel="next"')

    set_pagination_headers(response, link, total, filters['limit'])

    return data_list


def partially_update_attributes(instance: BaseModel, attributes: dict):
    for key, value in attributes.items():
        setattr(instance, key, value)

def encode_string_base64(input: str) -> str:
    input_bytes = base64.b64encode(bytes(input, 'utf-8'))
    return input_bytes.decode('utf-8')
