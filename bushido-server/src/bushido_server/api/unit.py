from fastapi import APIRouter

from bushido_server.api.deps import SessionDep
from bushido_server.schema.log_req import LogUnitRequest
from bushido_server.schema.log_res import UnitLogResponse
from bushido_server.service import log_unit

router = APIRouter()


@router.post("/log-unit")
async def process_log_request(
    request: LogUnitRequest, session: SessionDep
) -> UnitLogResponse:
    return log_unit(request, session)
