import urllib

from fastapi import Response

from py_ocpi.core.enums import ModuleID
from py_ocpi.core.config import settings
from py_ocpi.versions.enums import VersionNumber


def set_pagination_headers(response: Response, link: str, total: int, limit: int):
    response.headers['Link'] = link
    response.headers['X-Total-Count'] = str(total)
    response.headers['X-Limit'] = str(limit)
    return response


async def get_list(response: Response, filters: dict, module: ModuleID, version: VersionNumber, crud):
    data_list, total, is_last_page = await crud.list(module, filters)

    link = ''
    params = dict(**filters)
    params['offset'] = filters['offset'] + filters['limit']
    if not is_last_page:
        link = (f'<https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo'
                f'/{version}/{module}/?{urllib.parse.urlencode(params)}>; rel="next"')

    set_pagination_headers(response, link, total, filters['limit'])

    return data_list
