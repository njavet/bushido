from fastapi import APIRouter, HTTPException

from bushido_server.api.deps import SessionDep
from bushido_server.service import log_unit
from bushidolib.unit.base import BaseUnit, LogUnitRequest

router = APIRouter()


@router.post("/unit-logs")
async def process_log_request(request: LogUnitRequest, session: SessionDep) -> BaseUnit:
    try:
        return log_unit(request.line, session)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

