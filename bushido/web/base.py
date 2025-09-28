from fastapi import APIRouter, Depends, HTTPException, Path, Request
from sqlalchemy.orm import Session

from bushido.core.conf import UnitCategory
from bushido.web.deps import get_session
from bushido.core.result import Err
from bushido.schema.req import UnitLogRequest

router = APIRouter()


@router.post('/{unit_category}/log-unit')
async def log_unit(
    request: Request,
    ulr: UnitLogRequest,
    unit_category: UnitCategory,
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
