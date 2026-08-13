from fastapi import APIRouter


router = APIRouter()


@router.post("/log-unit")
async def log_unit(request: LogUnitRequest) -> UnitLogResponse:
    pass

