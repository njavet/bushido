from collections import defaultdict
from fastapi import Request, APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from bushido.service.base import BaseService
from bushido.data.conn import get_session
from bushido.utils.dt_functions import get_bushido_date_from_timestamp


router = APIRouter()



@router.post('/api/get_units')
async def log_unit(request: Request,
                   session: Session = Depends(get_session)):
    base_service = BaseService.from_session(session)
    units = base_service.get_units()

    dix = defaultdict(list)
    for unit in units:
        dt = get_bushido_date_from_timestamp(unit.timestamp)
        dix[dt].append((unit.emoji, unit.payload))
    return dix
