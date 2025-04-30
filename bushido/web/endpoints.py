from fastapi import Request, APIRouter, HTTPException

# project imports
from bushido.exceptions import ValidationError
from bushido.utils.parsing import preprocess_input


router = APIRouter()


@router.get('/api/emojis')
async def get_emojis(request: Request):
    return request.app.state.bot.get_all_emojis()


@router.get('/api/get_units')
async def get_units(request: Request):
    return request.app.state.bot.get_all_units()


@router.post('/api/log_unit')
async def log_unit(request: Request):
    with request.app.state.sf.get_session_context() as session:
        base_service = BaseService.from_session(session)
        data = await request.json()
        try:
            emoji, words, comment = preprocess_input(data['text'])
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))

        unit_name = base_service.unit_name_for_emoji(emoji)
        category = base_service.get_category_for_unit(unit_name)
        log_service = load_log_service(category).from_session(session)
        log_service.process_unit(unit_name, words, comment)
        return {'res': 'ok'}


