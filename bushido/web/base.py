from fastapi import APIRouter, Depends, HTTPException, Path, Request
from sqlalchemy.orm import Session

from bushido.core.deps import get_session
from bushido.core.result import Ok
from bushido.infra.repo.unit import UnitRepo
from bushido.schema.req import UnitLogRequest
from bushido.service.log_unit import LogUnitService

router = APIRouter()


@router.post('/{unit_name}/log-unit')
async def log_unit(
    request: Request,
    ulr: UnitLogRequest,
    session: Session = Depends(get_session),
) -> str | None:
    try:
        parser = request.app.state.parsers[unit_name]
        mapper = request.app.state.mappers[unit_name]
    except KeyError:
        raise HTTPException(status_code=404, detail='Unit not found')

    unit_repo = UnitRepo(session)
    service = LogUnitService(unit_repo, parser, mapper)
    result = service.log_unit(ulr.line)
    if isinstance(result, Ok):
        return result.value
    # TODO check return type
    raise HTTPException(status_code=400, detail=result.message)
