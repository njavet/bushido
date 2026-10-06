from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from citadel.api.deps import SessionDep, SpartanDep
from citadel.persistence.models import Spartan
from citadel.schema.res import SpartanResponse

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/spartans")
def get_spartans(
    session: SessionDep,
    spartan: SpartanDep,
) -> list[SpartanResponse]:
    if not spartan.is_admin:
        raise HTTPException(status_code=403, detail="Admin only")

    return list(session.scalars(select(Spartan).order_by(Spartan.id)))
