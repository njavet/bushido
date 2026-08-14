from fastapi import APIRouter
from sqlalchemy import select

from bushido_server.api.deps import SessionDep
from bushido_server.persistence.models import UnitSettingTable
from bushido_server.service import log_unit
from bushido_server.service.load_units import load_units
from bushidolib.contracts.load_req import LoadUnitRequest
from bushidolib.contracts.log_req import LogUnitRequest
from bushidolib.contracts.log_res import UnitLogResponse
from bushidolib.contracts.unit import LoadedUnits, UnitCategory, UnitSetting

router = APIRouter()


@router.get("/load-unit-settings")
async def process_load_unit_settings_request(session: SessionDep) -> list[UnitSetting]:
    # TODO refactor
    result = session.scalars(select(UnitSettingTable)).all()
    return [UnitSetting(name=r.name, category=UnitCategory(r.category)) for r in result]


@router.get("/load-units")
async def process_load_units_request(
    request: LoadUnitRequest, session: SessionDep
) -> LoadedUnits:
    return load_units(request, session)


@router.post("/log-unit")
async def process_log_request(
    request: LogUnitRequest, session: SessionDep
) -> UnitLogResponse:
    return log_unit(request, session)
