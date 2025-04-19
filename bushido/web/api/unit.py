from collections import defaultdict
from fastapi import Request, APIRouter
from bushido.service.unit import UnitService


router = APIRouter()


@router.get('/api/get_units')
async def get_units(request: Request):
    with request.app.state.sf.get_session_context() as session:
        base_service = UnitService.from_session(session)
        units = base_service.get_units()
        return units
