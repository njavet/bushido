from functools import singledispatch

from sqlalchemy.orm import Session

from bushido_server.persistence.repos import (
    CardioUnitRepo,
    GymUnitRepo,
    LiftingUnitRepo,
    WimhofUnitRepo,
)
from bushidolib.contracts.load_req import (
    CardioLoadUnitRequest,
    GymLoadUnitRequest,
    LiftingLoadUnitRequest,
    WimhofLoadUnitRequest,
)
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


@singledispatch
def load_units(request: object, _session: Session) -> LoadedUnits:
    raise TypeError(f"Unsupported type for load_units: {type(request).__name__}")


@load_units.register
def _(request: CardioLoadUnitRequest, session: Session) -> LoadedUnits:
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


@load_units.register
def _(request: GymLoadUnitRequest, session: Session) -> LoadedUnits:
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


@load_units.register
def _(request: LiftingLoadUnitRequest, session: Session) -> LoadedUnits:
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


@load_units.register
def _(request: WimhofLoadUnitRequest, session: Session) -> LoadedUnits:
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
