from fastapi import APIRouter, HTTPException

from citadel.api.v0.deps import SessionDep, SpartanDep
from citadel.schema.req import CommandRequest
from citadel.schema.res import LoggedUnit
from citadel.service import log_unit

router = APIRouter(tags=["command"])


@router.post("/command")
def process_command_request(
    request: CommandRequest,
    session: SessionDep,
    spartan: SpartanDep,
) -> LoggedUnit:
    try:
        return log_unit(request.line, session, spartan)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
