from pathlib import Path
import importlib
import importlib.util
from fastapi import Request, APIRouter, Depends
from sqlalchemy.orm import Session

# project imports
from bushido.exceptions import ValidationError, UploadError
from bushido.conf import KEIKO_PROCESSORS
from bushido.schema.base import UnitSpec
from bushido.service.unit import UnitService
from bushido.data.conn import get_session


router = APIRouter()


@router.get('/api/emojis')
async def get_emojis(session: Session = Depends(get_session)):
    service = UnitService.from_session(session)
    return service.get_all_emojis()


@router.post('/api/log_unit/{unit_name}')
async def log_unit(request: Request,
                   unit_spec: UnitSpec,
                   session: Session = Depends(get_session)):
    service = UnitService.from_session(session)
    category = service.get_category(unit_spec.unit_name)
    log_service = load_log_service(category).from_session(session)
    log_service.process(unit_spec)


def load_log_service(category: str, package: str = KEIKO_PROCESSORS) -> UnitService:
    spec = importlib.util.find_spec(package)
    if spec is None or not spec.submodule_search_locations:
        raise ImportError(f'Could not find package {package}')

    package_path = Path(spec.submodule_search_locations[0])
    module_name = f'{package}.{category}'
    module = importlib.import_module(module_name)

    if not hasattr(module, 'LogService'):
        raise ImportError(f'{module_name} does not define LogService')

    cls = getattr(module, 'KeikoProcessor')
    return cls
