from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

# project imports
from bushido.web.deps import get_session
from bushido.service.categories.lifting import UnitService


router = APIRouter()


@router.get('/api/get-lifting-units')
async def get_lifting_units(session: Session = Depends(get_session)):
    service = UnitService.from_session(session)
    return service.get_units()

