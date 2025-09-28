from fastapi import APIRouter, Depends, HTTPException, Request, Path
from sqlalchemy.orm import Session

from bushido.core.deps import get_session
from bushido.core.result import Err, Ok
from bushido.iface.parser.utils import preprocess_input
from bushido.infra.repo.unit import CompoundUnitRepo, UnitRepo
from bushido.schema.req import UnitLogRequest

router = APIRouter()


@router.post('/{unit_name}/log-unit')
async def log_unit(
    request: Request,
    ulr: UnitLogRequest,
    unit_name: str = Path(...),
    session: Session = Depends(get_session),
) -> str | None:

    try:
        service = request.app.state.services[unit_name]
    except KeyError:
        raise HTTPException(status_code=404, detail='Unit not found')

    result = service.log_unit(ulr.line, session)
    if isinstance(result, Err):
        raise HTTPException(status_code=400, detail=Err.message)
    return result.value
