import importlib
import importlib.util
from fastapi import Request, APIRouter, HTTPException
from bushido.exceptions import ValidationError, UploadError
from bushido.conf import KEIKO_PROCESSORS
from bushido.utils.parsing import preprocess_input
from bushido.service.base import BaseService


router = APIRouter()


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


def load_log_service(category: str, package: str = KEIKO_PROCESSORS):
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.submodule_search_locations:
        raise ImportError(f'Could not find package {package}')

    # package_path = Path(spec.submodule_search_locations[0])
    module_name = f'{package}.{category}'
    module = importlib.import_module(module_name)

    if not hasattr(module, 'LogService'):
        raise ImportError(f'{module_name} does not define LogService')

    cls = getattr(module, 'LogService')
    return cls
