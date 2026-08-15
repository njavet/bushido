import datetime

from sqlalchemy.orm import Session

from bushido_server.persistence.repos import (
    CardioUnitRepo,
    GymUnitRepo,
    LiftingUnitRepo,
    WimhofUnitRepo,
    load_unit_settings,
)
from bushido_server.schema.req import LogUnitRequest
from bushidolib.constants import UnitCategory
from bushidolib.contracts.log_res import UnitLogResponse
from bushidolib.contracts.unit import RawUnit
from bushidolib.domain import Unit
from bushidolib.domain.cardio import CardioData, parse_cardio_unit
from bushidolib.domain.gym import GymData, parse_gym_unit
from bushidolib.domain.lifting import LiftingData, parse_lifting_unit
from bushidolib.domain.parsing import parse_raw_unit, split_options
from bushidolib.domain.wimhof import WimhofData, parse_wimhof_unit
from bushidolib.exceptions import UnitParsingError

UnitData = LiftingData | GymData | CardioData | WimhofData
UnitRepo = CardioUnitRepo | GymUnitRepo | LiftingUnitRepo | WimhofUnitRepo


def log_unit(request: LogUnitRequest, session: Session) -> UnitLogResponse:
    unit_settings = {
        setting.name: setting.category for setting in load_unit_settings(session)
    }
    raw_unit = parse_raw_unit(request.line)
    raw_unit.tokens, log_time_str = split_options(raw_unit.tokens)
    if log_time_str is None:
        log_time = datetime.datetime.now(tz=datetime.UTC)
    else:
        log_time = datetime.datetime.strptime(log_time_str, "%Y%m%d-%H%M").replace(
            tzinfo=datetime.UTC
        )

    category = unit_settings.get(raw_unit.name)
    match category:
        case UnitCategory.CARDIO:
            return log_cardio_unit(raw_unit, log_time, session)
        case UnitCategory.GYM:
            return log_gym_unit(raw_unit, log_time, session)
        case UnitCategory.LIFTING:
            return log_lifting_unit(raw_unit, log_time, session)
        case UnitCategory.WIMHOF:
            return log_wimhof_unit(raw_unit, log_time, session)
        case _:
            raise UnitParsingError(f"Unknown unit: {raw_unit.name}")


def log_cardio_unit(
    raw_unit: RawUnit, log_time: datetime.datetime, session: Session
) -> UnitLogResponse:
    repo = CardioUnitRepo(session)
    repo.add_unit(
        Unit(
            name=raw_unit.name,
            data=parse_cardio_unit(raw_unit.tokens),
            log_time=log_time,
            comment=raw_unit.comment,
        )
    )
    return UnitLogResponse(status="OK")


def log_gym_unit(
    raw_unit: RawUnit, log_time: datetime.datetime, session: Session
) -> UnitLogResponse:
    repo = GymUnitRepo(session)
    repo.add_unit(
        Unit(
            name=raw_unit.name,
            data=parse_gym_unit(raw_unit.tokens),
            log_time=log_time,
            comment=raw_unit.comment,
        )
    )
    return UnitLogResponse(status="OK")


def log_lifting_unit(
    raw_unit: RawUnit, log_time: datetime.datetime, session: Session
) -> UnitLogResponse:
    repo = LiftingUnitRepo(session)
    repo.add_unit(
        Unit(
            name=raw_unit.name,
            data=parse_lifting_unit(raw_unit.tokens),
            log_time=log_time,
            comment=raw_unit.comment,
        )
    )
    return UnitLogResponse(status="OK")


def log_wimhof_unit(
    raw_unit: RawUnit, log_time: datetime.datetime, session: Session
) -> UnitLogResponse:
    repo = WimhofUnitRepo(session)
    repo.add_unit(
        Unit(
            name=raw_unit.name,
            data=parse_wimhof_unit(raw_unit.tokens),
            log_time=log_time,
            comment=raw_unit.comment,
        )
    )
    return UnitLogResponse(status="OK")
