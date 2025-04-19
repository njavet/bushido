from collections import defaultdict
from fastapi import Request, APIRouter
from bushido.utils.dt_functions import get_bushido_date_from_timestamp
from bushido.service.unit import UnitService


router = APIRouter()


@router.get('/api/get_units')
async def log_unit(request: Request):
    session = request.app.state.sf.get_session()
    base_service = UnitService.from_session(session)
    units = base_service.get_units()
    dix = defaultdict(list)
    for unit in units:
        dt = get_bushido_date_from_timestamp(unit.timestamp)
        dix[dt].append((unit.emoji, unit.payload))
    return dix
