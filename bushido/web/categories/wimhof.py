from sqlalchemy.orm import Session
from fastapi import Request, APIRouter, HTTPException, Depends

# project imports
from bushido.web.deps import get_session
from bushido.service import service


router = APIRouter()


@router.get('/api/wimhof-units')
async def get_wimhof_units(session: Session = Depends(get_session)):
    return service.get_units(session)
