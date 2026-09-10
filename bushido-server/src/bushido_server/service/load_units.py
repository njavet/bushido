from sqlalchemy.orm import Session

from bushido_server.persistence.repos import (
    CardioUnitRepo,
    GymUnitRepo,
    LiftingUnitRepo,
    WimhofUnitRepo,
)
from bushido_server.registry import CATEGORY_REGISTRY
from bushido_server.schema.req import LoadUnitRequest
from bushido_server.schema.res import LoadedUnits
from bushidolib.category.base import BaseUnit
from bushidolib.category.cardio import CardioData, CardioUnit
from bushidolib.category.gym import GymData, GymUnit
from bushidolib.category.lifting import LiftingData, LiftingUnit
from bushidolib.category.wimhof import WimhofData, WimhofUnit
from bushidolib.constants import UnitCategory


def load_units(request: LoadUnitRequest, session: Session) -> list[BaseUnit]:
    match request.unit_category:
        case UnitCategory.CARDIO:
            repo = CardioUnitRepo(session)
            return repo.fetch_units(start_t=request.start_time, end_t=request.end_time)
        case UnitCategory.GYM:
            repo = GymUnitRepo(session)
            return repo.fetch_units(start_t=request.start_time, end_t=request.end_time)
        case UnitCategory.LIFTING:
            repo = LiftingUnitRepo(session)
            return repo.fetch_units(start_t=request.start_time, end_t=request.end_time)
        case UnitCategory.WIMHOF:
            repo = WimhofUnitRepo(session)
            return repo.fetch_units(start_t=request.start_time, end_t=request.end_time)
        case _:
            raise ValueError(f"Unknown unit category: {request.unit_category}")

