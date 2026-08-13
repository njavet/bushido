from fastapi import APIRouter

from bushido_server.schema.log_req import LogUnitRequest
from bushido_server.schema.log_res import UnitLogResponse
from bushido_server.service import log_unit

router = APIRouter()


@router.post("/log-unit")
async def log_unit(request: LogUnitRequest) -> UnitLogResponse:
    return log_unit(request)
