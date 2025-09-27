from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from bushido.core.deps import get_mapper, get_parser, get_session
from bushido.core.result import Ok
from bushido.core.types import ORM_ST, ORM_T, UNIT_T
from bushido.iface.mapper.base import UnitMapper
from bushido.iface.parser.base import UnitParser
from bushido.infra.repo import UnitRepo
from bushido.schema.req import UnitLogRequest
from bushido.service.log_unit import LogUnitService

router = APIRouter()


@router.post('/{unit_name}/log-unit')
async def log_unit(
    ulr: UnitLogRequest,
    parser: UnitParser[UNIT_T] = Depends(get_parser),
    mapper: UnitMapper[UNIT_T, ORM_T, ORM_ST] = Depends(get_mapper),
    session: Session = Depends(get_session),
) -> str | None:
    unit_repo = UnitRepo(session)
    service = LogUnitService(unit_repo, parser, mapper)
    result = service.log_unit(ulr.line)
    if isinstance(result, Ok):
        return result.value
    # TODO check return type
    raise HTTPException(status_code=400, detail=result.message)
