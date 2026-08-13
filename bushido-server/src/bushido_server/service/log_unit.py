from functools import singledispatch

from sqlalchemy.orm import Session

from bushido_server.schema.log_req import (
    CardioLogUnitRequest,
    GymLogUnitRequest,
    LiftingLogUnitRequest,
    WimhofLogUnitRequest,
)
from bushido_server.schema.log_res import UnitLogResponse
from bushidolib.units import Unit


@singledispatch
def log_unit(request: object, _session: Session) -> UnitLogResponse:
    raise TypeError(f"Unsupported type for log_unit: {type(request).__name__}")


@log_unit.register
def _(request: CardioLogUnitRequest, session: Session) -> UnitLogResponse:
    pass


@log_unit.register
def _(request: GymLogUnitRequest, session: Session) -> UnitLogResponse:
    pass


@log_unit.register
def _(request: LiftingLogUnitRequest, session: Session) -> UnitLogResponse:
    pass


@log_unit.register
def _(request: WimhofLogUnitRequest, session: Session) -> UnitLogResponse:

    unit_data = unit_registry.parser.parse(tokens)
    unit = Unit(
        name=raw.name,
        emoji=unit_registry.emoji,
        data=unit_data,
        log_time=log_time,
        comment=raw.comment,
    )
    unit_registry.repo(session).add_unit(unit)
