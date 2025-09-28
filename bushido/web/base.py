from fastapi import APIRouter, Depends, HTTPException, Path, Request
from sqlalchemy.orm import Session

from bushido.core.result import Ok, Err
from bushido.core.deps import get_session
from bushido.infra.repo.unit import UnitRepo, CompoundUnitRepo
from bushido.iface.parser.utils import preprocess_input
from bushido.schema.req import UnitLogRequest
from bushido.service.log_unit import LogUnitService

router = APIRouter()


@router.post('/{unit_name}/log-unit')
async def log_unit(
    request: Request,
    ulr: UnitLogRequest,
    session: Session = Depends(get_session),
) -> str | None:
    pre_result = preprocess_input(ulr.line)
    if isinstance(pre_result, Err):
        raise HTTPException(status_code=404, detail=pre_result.message)

    unit_spec = pre_result.value
    try:
        parser = request.app.state.parsers[unit_spec.name]
        mapper = request.app.state.mappers[unit_spec.name]
    except KeyError:
        raise HTTPException(status_code=404, detail='Unit not found')

    parse_result = parser.parse(unit_spec)
    if isinstance(parse_result, Err):
        raise HTTPException(status_code=404, detail=parse_result.message)

    parsed_unit = parse_result.value
    if parsed_unit.compound:
        unit, subunits = mapper.to_orm(parsed_unit)
        unit_repo = CompoundUnitRepo(session)
        result = unit_repo.add_compound_unit(unit, subunits)
    else:
        unit = mapper.to_orm(parsed_unit)
        unit_repo = UnitRepo(session)
        result = unit_repo.add_unit(unit)
    if result:
        return 'Unit Confirmed'
    # TODO check return type
    raise HTTPException(status_code=400, detail='Error')
