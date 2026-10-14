from fastapi import APIRouter, HTTPException

from citadel.api.v0.deps import SessionDep, SpartanDep
from citadel.registry import UNIT_REGISTRY
from citadel.schema.req import LoadUnitRequest, LogUnitRequest
from citadel.schema.res import LoggedUnit, UnitsPerDay
from citadel.service import load_units, log_unit

router = APIRouter(prefix="/unit", tags=["unit"])


@router.get("/names")
def get_unit_names() -> list[str]:
    return list(UNIT_REGISTRY.keys())


@router.get("/help")
def get_help() -> None:
    pass
