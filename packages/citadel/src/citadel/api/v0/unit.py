from fastapi import APIRouter, HTTPException

from citadel.api.deps import SessionDep, SpartanDep
from citadel.domain.dtypes import LoggedUnit
from citadel.registry import UNIT_REGISTRY
from citadel.schema.req import LoadUnitRequest, LogUnitRequest
from citadel.service import load_units, log_unit

router = APIRouter(prefix="/unit", tags=["unit"])


@router.get("/names")
def get_unit_names() -> list[str]:
    return list(UNIT_REGISTRY.keys())


@router.post("/logs")
async def process_log_request(
    request: LogUnitRequest,
    session: SessionDep,
    spartan: SpartanDep,
) -> LoggedUnit:
    try:
        return log_unit(request.line, session, spartan)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/logs/query")
async def process_load_units_request(
    request: LoadUnitRequest,
    session: SessionDep,
    spartan: SpartanDep,
) -> list[LoggedUnit]:
    try:
        return load_units(request, session, spartan)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
