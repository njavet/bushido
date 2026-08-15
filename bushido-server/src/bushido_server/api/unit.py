from fastapi import APIRouter

from bushido_server.api.deps import SessionDep
from bushido_server.schema.req import LoadUnitRequest, LogUnitRequest
from bushido_server.schema.res import LoadedUnits
from bushido_server.service import log_unit
from bushido_server.service.load_unit_settings import load_unit_mappings
from bushido_server.service.load_units import load_units
from bushidolib.contracts import LoggedUnit
from bushidolib.unit import UnitSetting

router = APIRouter()


@router.get("/unit-settings")
async def process_load_unit_settings_request(session: SessionDep) -> list[UnitSetting]:
    return load_unit_mappings(session)


@router.post("/unit-logs")
async def process_log_request(
    request: LogUnitRequest, session: SessionDep
) -> LoggedUnit:
    return log_unit(request.line, session)


@router.post("/unit-logs/query")
async def process_load_units_request(
    request: LoadUnitRequest, session: SessionDep
) -> LoadedUnits:
    return load_units(request, session)
