from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from bushido.core.conf import UnitCategory
from bushido.domain.result import Err
from bushido.schema.req import UnitLogRequest
from bushido.service.factory import ServiceFactory
from bushido.web.deps import get_session

router = APIRouter()


@router.post("/{unit_category}/log-unit")
async def log_unit(
    ulr: UnitLogRequest,
    unit_category: UnitCategory,
    session: Session = Depends(get_session),
) -> str | None:
    svc_res = ServiceFactory().get_service(unit_category, session)
    if isinstance(svc_res, Err):
        raise HTTPException(status_code=404, detail=Err.message)
    service = svc_res.value
    result = service.log_unit(ulr.line)
    if isinstance(result, Err):
        raise HTTPException(status_code=400, detail=Err.message)
    return result.value
