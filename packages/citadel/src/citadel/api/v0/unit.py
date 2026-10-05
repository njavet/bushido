from fastapi import APIRouter, HTTPException

from citadel.api.deps import SessionDep, UserDep
from citadel.domain.dtypes import LoggedUnit
from citadel.registry import UNIT_REGISTRY
from citadel.schema.req import LogUnitRequest
from citadel.service import log_unit

router = APIRouter()


@router.get("/unit-names")
def get_unit_names() -> list[str]:
    return list(UNIT_REGISTRY.keys())


@router.post("/unit-logs")
async def process_log_request(
    request: LogUnitRequest,
    session: SessionDep,
    spartan: UserDep,
) -> LoggedUnit:
    try:
        return log_unit(request.line, session, spartan)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
