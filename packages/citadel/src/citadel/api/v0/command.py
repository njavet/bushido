from fastapi import APIRouter, HTTPException

from citadel.api.v0.deps import SessionDep, SpartanDep
from citadel.registry import UNIT_REGISTRY
from citadel.schema.req import LoadUnitRequest, CommandRequest
from citadel.schema.res import LoggedUnit, UnitsPerDay
from citadel.service import load_units, process_command

router = APIRouter(prefix="/command", tags=["command"])


@router.post("/command")
def process_command_request(
    request: CommandRequest,
    session: SessionDep,
    spartan: SpartanDep,
) -> LoggedUnit:
    try:
        return process_command(request.line, session, spartan)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
