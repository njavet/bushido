from fastapi import Request, APIRouter, HTTPException

# project imports
from bushido.exceptions import ValidationError
from bushido.schema.req import UnitLogRequest
from bushido.service.unit import BaseUnitService


router = APIRouter()


@router.get('/api/get-categories')
async def get_emojis(request: Request):
    repo = request.app.state.bot.get_repo()
    service = BaseUnitService(repo)
    return service.get_all_categories()


@router.get('/api/get-emojis')
async def get_emojis(request: Request):
    repo = request.app.state.bot.get_repo()
    service = BaseUnitService(repo)
    return service.get_all_emojis()


@router.get('/api/get-units')
async def get_units(request: Request):
    repo = request.app.state.bot.get_repo()
    service = BaseUnitService(repo)
    return service.get_units()


@router.post('/api/log-unit')
async def log_unit(request: Request, unit_log_request: UnitLogRequest):
    try:
        unit_log_res = request.app.state.bot.log_unit(unit_log_request.text)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return unit_log_res
