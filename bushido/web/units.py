import datetime
from zoneinfo import ZoneInfo
from fastapi import Request, APIRouter

# project imports
from bushido.conf import LOCAL_TIME_ZONE
from bushido.exceptions import ValidationError, UploadError
from bushido.schema.base import UnitSpec


router = APIRouter()


def create_unit_spec(unit_name, words, comment):
    now = datetime.datetime.now().replace(tzinfo=LOCAL_TIME_ZONE)
    timestamp = int(now.timestamp())
    unit_spec = UnitSpec(timestamp=timestamp,
                         unit_name=unit_name,
                         words=words,
                         comment=comment)
    return unit_spec


@router.post('/log_unit')
async def log_unit(request: Request):
    data = await request.json()
    up = request.app.state.up
    try:
        unit_name, words, comment = up.preprocess_input(data['text'])
    except ValidationError as e:
        return {'status': 'error', 'message': str(e)}

    try:
        unit_spec = create_unit_spec(unit_name, words, comment)
        up.process_input(unit_spec)
    except ValidationError as e:
        return {'status': 'error', 'message': str(e)}
    except UploadError as e:
        return {'status': 'success', 'message': str(e)}


@router.get('/emojis')
async def get_emojis(request: Request):
    emoji_specs = request.app.state.dm.load_emojis()
    lst = []
    for emoji_spec in emoji_specs:
        dix = {'key': emoji_spec.unit_name,
               'value': emoji_spec.emoji}
        lst.append(dix)
    return lst


@router.get('/units')
async def get_units(request: Request):
    dm = request.app.state.dm
    units = dm.retrieve_all_units()
