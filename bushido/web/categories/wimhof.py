from sqlalchemy.orm import Session
from fastapi import Request, APIRouter, HTTPException, Depends

# project imports
from bushido.web.deps import get_session
from bushido.service.categories.wimhof import UnitService


router = APIRouter()


@router.get('/api/get-wimhof-units')
async def get_wimhof_units(session: Session = Depends(get_session)):
    service = UnitService.from_session(session)
    return service.get_units()

