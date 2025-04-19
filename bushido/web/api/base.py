from fastapi import APIRouter, Request
from bushido.service.base import BaseService


router = APIRouter()


@router.get('/api/emojis')
async def get_emojis(request: Request):
    with request.app.state.sf.get_session_context() as session:
        service = BaseService.from_session(session)
        return service.get_all_emojis()
