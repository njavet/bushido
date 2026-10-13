from fastapi import APIRouter, HTTPException

from citadel.api.v0.deps import SessionDep, SpartanDep
from citadel.registry import UNIT_REGISTRY
from citadel.schema.req import LoadUnitRequest
from citadel.schema.res import UnitsPerDay
from citadel.service import load_units

router = APIRouter(prefix="/unit", tags=["unit"])


@router.get("/names")
def get_unit_names() -> list[str]:
    return list(UNIT_REGISTRY.keys())


@router.post("/logs/query")
def process_load_units_request(
    request: LoadUnitRequest,
    session: SessionDep,
    spartan: SpartanDep,
) -> list[UnitsPerDay]:
    try:
        return load_units(request, session, spartan)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
