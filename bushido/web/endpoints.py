from fastapi import Request, APIRouter, HTTPException

# project imports
from bushido.exceptions import ValidationError


router = APIRouter()


@router.get('/api/emojis')
async def get_emojis(request: Request):
    return request.app.state.bot.get_all_emojis()


@router.get('/api/get_units')
async def get_units(request: Request):
    return request.app.state.bot.get_all_units()


@router.post('/api/log_unit')
async def log_unit(request: Request):
    data = await request.json()
    try:
        request.app.state.bot.log_unit(data['text'])
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {'res': 'ok'}
