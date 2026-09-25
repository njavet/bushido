from bushidolib.unit.base import BaseUnit, LogUnitRequest
from fastapi import APIRouter, HTTPException

from citadel.api.deps import SessionDep
from citadel.registry import UNIT_REGISTRY
from citadel.service import log_unit

router = APIRouter()


@router.get("/unit-names")
def get_unit_names() -> list[str]:
    return list(UNIT_REGISTRY.keys())


@router.post("/unit-logs")
async def process_log_request(request: LogUnitRequest, session: SessionDep) -> BaseUnit:
    try:
        return log_unit(request.line, session)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
