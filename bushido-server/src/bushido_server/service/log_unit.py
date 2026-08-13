from functools import singledispatch

from sqlalchemy.orm import Session

from bushido_server.schema.log_req import (
    CardioLogUnitRequest,
    GymLogUnitRequest,
    LiftingLogUnitRequest,
    WimhofLogUnitRequest,
)
from bushido_server.schema.log_res import UnitLogResponse
from bushido_server.persistence.repos import CardioUnitRepo
from bushidolib.units import Unit
from bushidolib.units.cardio import parse_cardio_unit


@singledispatch
def log_unit(request: object, _session: Session) -> UnitLogResponse:
    raise TypeError(f"Unsupported type for log_unit: {type(request).__name__}")


@log_unit.register
def _(request: CardioLogUnitRequest, session: Session) -> UnitLogResponse:
    cardio_data = parse_cardio_unit(request.tokens)
    repo = CardioUnitRepo(session)
    repo.add_unit(Unit(
        name=request.unit_name,
        data=cardio_data,
        log_time=request.log_time,
        comment=request.comment,
    ))
    return UnitLogResponse(status="OK")


@log_unit.register
def _(request: GymLogUnitRequest, session: Session) -> UnitLogResponse:
    pass


@log_unit.register
def _(request: LiftingLogUnitRequest, session: Session) -> UnitLogResponse:
    pass


@log_unit.register
def _(request: WimhofLogUnitRequest, session: Session) -> UnitLogResponse:

    unit_data = unit_registry.parser.parse(tokens)
    unit_registry.repo(session).add_unit(unit)
