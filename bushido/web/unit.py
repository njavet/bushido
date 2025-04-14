from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session

# project imports
from bushido.exceptions import ValidationError, UploadError
from bushido.schema.base import UnitSpec
from bushido.service.unit import UnitService
from bushido.data.conn import get_session


router = APIRouter()


@router.get('/api/emojis')
async def get_emojis(session: Session = Depends(get_session)):
    service = UnitService.from_session(session)
    return service.get_all_emojis()


@router.post('/api/log_unit/{unit_name}')
async def log_unit(request: Request, unit_spec: UnitSpec):
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
