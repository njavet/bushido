from sqlalchemy.orm import Session

from bushido_server.persistence.repos import (
    CardioUnitRepo,
    GymUnitRepo,
    LiftingUnitRepo,
    WimhofUnitRepo,
)
from bushido_server.schema.req import LoadUnitRequest
from bushidolib.constants import UnitCategory
from bushidolib.contracts.unit import (
    CardioData,
    CardioUnit,
    GymData,
    GymUnit,
    LiftingData,
    LiftingUnit,
    LoadedUnits,
    WimhofData,
    WimhofUnit,
)


def load_units(request: LoadUnitRequest, session: Session) -> LoadedUnits:
    match request.unit_category:
        case UnitCategory.CARDIO:
            return load_cardio_units(request, session)
        case UnitCategory.GYM:
            return load_cardio_units(request, session)
        case UnitCategory.LIFTING:
            return load_cardio_units(request, session)
        case UnitCategory.WIMHOF:
            return load_cardio_units(request, session)
        case _:
            raise ValueError(f"Unknown unit category: {request.unit_category}")


def load_cardio_units(request: LoadUnitRequest, session: Session) -> list[CardioUnit]:
    repo = CardioUnitRepo(session)
    units = repo.fetch_units(start_t=request.start_time, end_t=request.end_time)
    return [
        CardioUnit(
            name=unit.name,
            log_time=unit.log_time,
            comment=unit.comment,
            data=CardioData.model_validate(unit.data),
        )
        for unit in units
    ]


def load_gym_units(request: LoadUnitRequest, session: Session) -> list[GymUnit]:
    repo = GymUnitRepo(session)
    units = repo.fetch_units(start_t=request.start_time, end_t=request.end_time)
    return [
        GymUnit(
            name=unit.name,
            log_time=unit.log_time,
            comment=unit.comment,
            data=GymData.model_validate(unit.data),
        )
        for unit in units
    ]


def load_lifting_units(request: LoadUnitRequest, session: Session) -> list[LiftingUnit]:
    repo = LiftingUnitRepo(session)
    units = repo.fetch_units(start_t=request.start_time, end_t=request.end_time)
    return [
        LiftingUnit(
            name=unit.name,
            log_time=unit.log_time,
            comment=unit.comment,
            data=LiftingData.model_validate(unit.data),
        )
        for unit in units
    ]


def load_wimhof_units(request: LoadUnitRequest, session: Session) -> list[WimhofUnit]:
    repo = WimhofUnitRepo(session)
    units = repo.fetch_units(start_t=request.start_time, end_t=request.end_time)
    return [
        WimhofUnit(
            name=unit.name,
            log_time=unit.log_time,
            comment=unit.comment,
            data=WimhofData.model_validate(unit.data),
        )
        for unit in units
    ]
