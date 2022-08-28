from fastapi import APIRouter, Depends, Response, Request
from pydantic import ValidationError

from py_ocpi.versions.enums import VersionNumber
from py_ocpi.core.utils import get_auth_token, get_list
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.enums import ModuleID
from py_ocpi.core.dependencies import get_crud, get_adapter, pagination_filters

router = APIRouter(
    prefix='/cdrs',
)


@router.get("/", response_model=OCPIResponse)
async def get_cdrs(response: Response,
                   request: Request,
                   crud=Depends(get_crud),
                   adapter=Depends(get_adapter),
                   filters: dict = Depends(pagination_filters)):
    try:
        token = get_auth_token(request)
        data_list = await get_list(response, filters, ModuleID.cdrs,
                                   VersionNumber.v_2_2_1, crud, token=token)

        cdrs = []
        for data in data_list:
            cdrs.append(adapter.cdr_adapter(data).dict())
        return OCPIResponse(
            data=cdrs,
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )
