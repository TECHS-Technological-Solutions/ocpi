import importlib
import urllib
import base64
from typing import Union, Any

from fastapi import Response, Request
from pydantic import BaseModel

from py_ocpi.core.config import logger
from py_ocpi.core.enums import ModuleID, RoleEnum
from py_ocpi.core.config import settings
from py_ocpi.modules.versions.enums import VersionNumber


def set_pagination_headers(
    response: Response, link: str, total: int, limit: int
):
    response.headers["Link"] = link
    response.headers["X-Total-Count"] = str(total)
    response.headers["X-Limit"] = str(limit)
    return response


def get_auth_token(
    request: Request,
    version: VersionNumber = VersionNumber.v_2_2_1,
) -> Union[str, None]:
    headers = request.headers
    headers_token = headers.get("authorization", "Token Null")
    token = headers_token.split()[1]
    if token == "Null":  # nosec
        return None
    if version.startswith("2.1") or version.startswith("2.0"):
        return token
    return decode_string_base64(token)


async def get_list(
    response: Response,
    filters: dict,
    module: ModuleID,
    role: RoleEnum,
    version: VersionNumber,
    crud,
    *args,
    **kwargs,
):
    data_list, total, is_last_page = await crud.list(
        module, role, filters, *args, version=version, **kwargs
    )

    link = ""
    params = dict(**filters)
    params["offset"] = filters["offset"] + filters["limit"]
    if not is_last_page:
        link = (
            f"<https://{settings.OCPI_HOST}/{settings.OCPI_PREFIX}/cpo"
            f"/{version}/{module}/"
            f'?{urllib.parse.urlencode(params)}>; rel="next"'  # type: ignore
        )

    set_pagination_headers(response, link, total, filters["limit"])
    logger.debug(
        f"List / total / is_last_page -> "
        f"{len(data_list)} / {total} / {is_last_page}."
    )
    return data_list


def partially_update_attributes(instance: BaseModel, attributes: dict):
    for key, value in attributes.items():
        setattr(instance, key, value)


def encode_string_base64(input: str) -> str:
    input_bytes = base64.b64encode(bytes(input, "utf-8"))
    return input_bytes.decode("utf-8")


def decode_string_base64(input: str) -> str:
    input_bytes = base64.b64decode(bytes(input, "utf-8"))
    return input_bytes.decode("utf-8")


def get_module_model(class_name, module_name: str, version_name: str) -> Any:
    module_dir = f"py_ocpi.modules.{module_name}.{version_name}.schemas"
    try:
        module = importlib.import_module(module_dir)
        return getattr(module, class_name)
    except ImportError:
        raise NotImplementedError(
            f"{class_name} schema for version {version_name} not found.",
        )
