from fastapi import APIRouter

from bushido_server.api.deps import SessionDep
from bushido_server.service import log_unit
from bushidolib.contracts.log_req import LogUnitRequest
from bushidolib.contracts.log_res import UnitLogResponse

router = APIRouter()


@router.get("/get-units")
async def get_units() -> dict[str, str]:
    pass


@router.post("/log-unit")
async def process_log_request(
    request: LogUnitRequest, session: SessionDep
) -> UnitLogResponse:
    return log_unit(request, session)
