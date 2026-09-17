from sqlalchemy.orm import Session

from bushido_server.persistence.repos import (
    CardioUnitRepo,
    GymUnitRepo,
    LiftingUnitRepo,
    WimhofUnitRepo,
)
from bushido_server.schema.res import LoadedUnits
from bushidolib.constants import UnitCategory
from bushidolib.schema.req import LoadUnitRequest


def load_units(request: LoadUnitRequest, session: Session) -> LoadedUnits:
    match request.unit_category:
        case UnitCategory.CARDIO:
            return CardioUnitRepo(session).fetch_units(
                start_t=request.start_time, end_t=request.end_time
            )
        case UnitCategory.GYM:
            return GymUnitRepo(session).fetch_units(
                start_t=request.start_time, end_t=request.end_time
            )
        case UnitCategory.LIFTING:
            return LiftingUnitRepo(session).fetch_units(
                start_t=request.start_time, end_t=request.end_time
            )
        case UnitCategory.WIMHOF:
            return WimhofUnitRepo(session).fetch_units(
                start_t=request.start_time, end_t=request.end_time
            )
        case _:
            raise ValueError(f"Unknown unit category: {request.unit_category}")
