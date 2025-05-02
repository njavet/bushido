from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

# project imports
from bushido.web.deps import get_session
from bushido.service.categories.lifting import UnitService


router = APIRouter()


@router.get('/api/get-lifting-units')
async def get_lifting_sets(session: Session = Depends(get_session)):
    service = UnitService.from_session(session)
    return service.get_sets()


@router.get('/api/get-5x5')
async def get_5x5(session: Session = Depends(get_session)):
    service = UnitService.from_session(session)
    res = service.get_completed_5x5()
    for unit_name, sessions in res.items():
        print('unit_name', unit_name)
        for ts, w, r in sessions:
            print(w, r)
    return res

