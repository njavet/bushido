from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from bushido.service.base import BaseService
from bushido.data.conn import get_session


router = APIRouter()


@router.get('/api/emojis')
async def get_emojis(session: Session = Depends(get_session)):
    service = BaseService.from_session(session)
    return service.get_all_emojis()
