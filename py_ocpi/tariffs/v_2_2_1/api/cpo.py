from fastapi import APIRouter, Depends, Response
from pydantic import ValidationError

from py_ocpi.core.utils import get_list
from py_ocpi.core import status
from py_ocpi.core.schemas import OCPIResponse
from py_ocpi.core.enums import ModuleID
from py_ocpi.core.dependencies import get_crud, get_adapter, pagination_filters
from py_ocpi.versions.enums import VersionNumber

router = APIRouter(
    prefix='/tariffs',
)


@router.get("/", response_model=OCPIResponse)
async def get_tariffs(response: Response,
                      crud=Depends(get_crud),
                      adapter=Depends(get_adapter),
                      filters: dict = Depends(pagination_filters)):
    try:
        data_list = await get_list(response, filters, ModuleID.tariffs,
                                   VersionNumber.v_2_2_1, crud)

        tariffs = []
        for data in data_list:
            tariffs.append(adapter.tariff_adapter(data).dict())
        return OCPIResponse(
            data=tariffs,
            **status.OCPI_1000_GENERIC_SUCESS_CODE,
        )
    except ValidationError:
        return OCPIResponse(
            data=[],
            **status.OCPI_3001_UNABLE_TO_USE_CLIENTS_API,
        )
