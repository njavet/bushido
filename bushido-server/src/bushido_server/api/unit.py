from bushidolib.contracts import LoggedUnit
from fastapi import APIRouter, HTTPException

from bushido_server.api.deps import SessionDep
from bushido_server.schema.req import LoadUnitRequest, LogUnitRequest
from bushido_server.schema.res import LoadedUnits
from bushido_server.service import log_unit
from bushido_server.service.load_units import load_units

router = APIRouter()


@router.post("/unit-logs")
async def process_log_request(
    request: LogUnitRequest, session: SessionDep
) -> LoggedUnit:
    try:
        return log_unit(request.line, session)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/unit-logs/query")
async def process_load_units_request(
    request: LoadUnitRequest, session: SessionDep
) -> LoadedUnits:
    try:
        return load_units(request, session)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
