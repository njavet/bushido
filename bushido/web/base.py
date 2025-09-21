from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from bushido.core.deps import get_mapper, get_parser, get_session
from bushido.core.result import Ok
from bushido.repo.base import UnitRepo
from bushido.schema.req import UnitLogRequest
from bushido.service.log_unit import LogUnitService
from bushido.service.mapper.base import UnitMapper
from bushido.service.parser.base import UnitParser

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
