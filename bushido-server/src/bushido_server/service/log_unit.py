from functools import singledispatch
from typing import Any

from sqlalchemy.orm import Session

from bushido_server.persistence.repos import (
    CardioUnitRepo,
    GymUnitRepo,
    LiftingUnitRepo,
    WimhofUnitRepo,
)
from bushido_server.schema.log_req import (
    CardioLogUnitRequest,
    GymLogUnitRequest,
    LiftingLogUnitRequest,
    WimhofLogUnitRequest,
)
from bushido_server.schema.log_res import UnitLogResponse
from bushidolib.domain import Unit
from bushidolib.domain.cardio import parse_cardio_unit
from bushidolib.domain.gym import parse_gym_unit
from bushidolib.domain.lifting import parse_lifting_unit
from bushidolib.domain.wimhof import parse_wimhof_unit


@singledispatch
def log_unit(request: object, _session: Session) -> UnitLogResponse:
    raise TypeError(f"Unsupported type for log_unit: {type(request).__name__}")


@log_unit.register
def _(request: CardioLogUnitRequest, session: Session) -> UnitLogResponse:
    cardio_data = parse_cardio_unit(request.tokens)
    repo = CardioUnitRepo(session)
    return _add_unit(request, cardio_data, repo)


@log_unit.register
def _(request: GymLogUnitRequest, session: Session) -> UnitLogResponse:
    gym_data = parse_gym_unit(request.tokens)
    repo = GymUnitRepo(session)
    return _add_unit(request, gym_data, repo)


@log_unit.register
def _(request: LiftingLogUnitRequest, session: Session) -> UnitLogResponse:
    lifting_data = parse_lifting_unit(request.tokens)
    repo = LiftingUnitRepo(session)
    return _add_unit(request, lifting_data, repo)


@log_unit.register
def _(request: WimhofLogUnitRequest, session: Session) -> UnitLogResponse:
    wimhof_data = parse_wimhof_unit(request.tokens)
    repo = WimhofUnitRepo(session)
    return _add_unit(request, wimhof_data, repo)


def _add_unit(request: Any, data: Any, repo: Any) -> UnitLogResponse:
    repo.add_unit(
        Unit(
            name=request.unit_name,
            data=data,
            log_time=request.log_time,
            comment=request.comment,
        )
    )
    return UnitLogResponse(status="OK")
