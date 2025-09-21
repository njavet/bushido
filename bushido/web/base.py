from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException
from fastapi import APIRouter

from bushido.core.deps import get_parser, get_mapper, get_session
from bushido.core.result import Ok
from bushido.repo.base import UnitRepo
from bushido.service.log_unit import LogUnitService
from bushido.service.parser.base import UnitParser
from bushido.service.mapper.base import UnitMapper
from bushido.schema.req import UnitLogRequest

router = APIRouter()


@router.post('/{unit_name}/log-unit')
async def log_unit(
    ulr: UnitLogRequest,
    parser: UnitParser = Depends(get_parser),
    mapper: UnitMapper = Depends(get_mapper),
    session: Session = Depends(get_session),
):
    unit_repo = UnitRepo(session=session)
    service = LogUnitService(unit_repo, parser, mapper)
    result = service.log_unit(ulr.line)
    if isinstance(result, Ok):
        return result.value

    raise HTTPException(status_code=400, detail=result.message)
