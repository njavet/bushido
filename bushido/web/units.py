import datetime
from zoneinfo import ZoneInfo
from fastapi import Request, APIRouter

# project imports
from bushido.exceptions import ValidationError
from bushido.schema.base import UnitSpec
from bushido.service.setup import load_keiko_processors_from_package


router = APIRouter()


def create_unit_spec(unit_name, words, comment):
    now = datetime.datetime.now().replace(tzinfo=ZoneInfo('Europe/Zurich'))
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
        unit_name, words, comment = up.preprocess_input(data)
    except ValidationError as e:
        return {'status': 'error', 'message': str(e)}

    unit_spec = create_unit_spec(unit_name, words, comment)
    res = up.process_unit(unit_spec)
    return {'status': 'success', 'res': res}
