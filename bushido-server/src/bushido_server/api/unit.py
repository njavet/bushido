from fastapi import APIRouter

from bushido_server.api.deps import SessionDep
from bushido_server.service import log_unit
from bushidolib.contracts.load_req import LoadUnitRequest
from bushidolib.contracts.log_req import LogUnitRequest
from bushidolib.contracts.log_res import UnitLogResponse
from bushidolib.contracts.unit import UnitSetting, LoadedUnits

router = APIRouter()


@router.get("/load-unit-settings")
async def process_load_unit_settings_request(session: SessionDep) -> list[UnitSetting]:
    pass


@router.get("/load-units")
async def process_load_units_request(request: LoadUnitRequest, session: SessionDep) -> LoadedUnits:
    pass


@router.post("/log-unit")
async def process_log_request(
    request: LogUnitRequest, session: SessionDep
) -> UnitLogResponse:
    return log_unit(request, session)
