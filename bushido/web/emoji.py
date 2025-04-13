from fastapi import Request, APIRouter


router = APIRouter()


@router.get('/api/emojis')
async def get_emojis(request: Request):
    emoji_specs = request.app.state.dm.load_emojis()
    lst = []
    for emoji_spec in emoji_specs:
        dix = {'key': emoji_spec.unit_name,
               'value': emoji_spec.emoji}
        lst.append(dix)
    return lst

