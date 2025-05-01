from sqlalchemy.orm import Session
from fastapi import APIRouter, HTTPException, Depends

# project imports
from bushido.exceptions import ValidationError
from bushido.schema.req import UnitLogRequest
from bushido.service import service
from bushido.web.deps import get_session


router = APIRouter()


@router.get('/api/get-categories')
async def get_categories_service(session: Session = Depends(get_session)):
    return service.get_categories(session)


@router.get('/api/get-emojis')
async def get_emojis_service(session: Session = Depends(get_session)):
    return service.get_emojis(session)


@router.get('/api/get-units')
async def get_units_service(session: Session = Depends(get_session)):
    return service.get_units(session)


@router.post('/api/log-unit')
async def log_unit_service(unit_log_request: UnitLogRequest,
                           session: Session = Depends(get_session)):
    try:
        unit_log_res = service.log_unit(unit_log_request.text, session)
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return unit_log_res
