from typing import Any

from sqlalchemy.orm import Session

from bushido_server.persistence.repos import (
    CardioUnitRepo,
    GymUnitRepo,
    LiftingUnitRepo,
    WimhofUnitRepo,
)
from bushido_server.service.load_unit_settings import load_unit_settings
from bushidolib.constants import UnitCategory
from bushidolib.contracts.log_res import UnitLogResponse
from bushidolib.contracts.req import LogUnitRequest
from bushidolib.domain import Unit
from bushidolib.domain.cardio import CardioData, parse_cardio_unit
from bushidolib.domain.gym import GymData, parse_gym_unit
from bushidolib.domain.lifting import LiftingData, parse_lifting_unit
from bushidolib.domain.wimhof import WimhofData, parse_wimhof_unit
from bushidolib.exceptions import ParsingUnitError

UnitData = LiftingData | GymData | CardioData | WimhofData
UnitRepo = CardioUnitRepo | GymUnitRepo | LiftingUnitRepo | WimhofUnitRepo


def log_unit(request: LogUnitRequest, session: Session) -> UnitLogResponse:
    unit_settings = {
        setting.name: setting.category for setting in load_unit_settings(session)
    }
    category = unit_settings.get(request.unit_name)
    match category:
        case UnitCategory.CARDIO:
            return log_cardio_unit(request, session)
        case UnitCategory.GYM:
            return log_gym_unit(request, session)
        case UnitCategory.LIFTING:
            return log_lifting_unit(request, session)
        case UnitCategory.WIMHOF:
            return log_wimhof_unit(request, session)
        case _:
            raise ParsingUnitError(f"Unknown unit: {request.unit_name}")


def log_cardio_unit(request: LogUnitRequest, session: Session) -> UnitLogResponse:
    cardio_data = parse_cardio_unit(request.tokens)
    repo = CardioUnitRepo(session)
    return _add_unit(request, cardio_data, repo)


def log_gym_unit(request: LogUnitRequest, session: Session) -> UnitLogResponse:
    gym_data = parse_gym_unit(request.tokens)
    repo = GymUnitRepo(session)
    return _add_unit(request, gym_data, repo)


def log_lifting_unit(request: LogUnitRequest, session: Session) -> UnitLogResponse:
    lifting_data = parse_lifting_unit(request.tokens)
    repo = LiftingUnitRepo(session)
    return _add_unit(request, lifting_data, repo)


def log_wimhof_unit(request: LogUnitRequest, session: Session) -> UnitLogResponse:
    wimhof_data = parse_wimhof_unit(request.tokens)
    repo = WimhofUnitRepo(session)
    return _add_unit(request, wimhof_data, repo)


def _add_unit(request: LogUnitRequest, data: UnitData, repo: Any) -> UnitLogResponse:
    repo.add_unit(
        Unit(
            name=request.unit_name,
            data=data,
            log_time=request.log_time,
            comment=request.comment,
        )
    )
    return UnitLogResponse(status="OK")
