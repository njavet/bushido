from fastapi import APIRouter

from bushido_server.schema.log_req import LogUnitRequest
from bushido_server.schema.log_res import UnitLogResponse

router = APIRouter()


@router.post("/log-unit")
async def log_unit(request: LogUnitRequest) -> UnitLogResponse:
    pass
