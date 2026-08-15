import datetime

from sqlalchemy.orm import Session

from bushido_server.persistence.repos import (
    CardioUnitRepo,
    GymUnitRepo,
    LiftingUnitRepo,
    WimhofUnitRepo,
    load_unit_settings,
)
from bushidolib.cardio import CardioData, CardioUnit, parse_cardio_unit
from bushidolib.constants import UnitCategory
from bushidolib.contracts import LoggedUnit
from bushidolib.exceptions import UnitParsingError
from bushidolib.gym import GymData, GymUnit, parse_gym_unit
from bushidolib.lifting import LiftingData, LiftingUnit, parse_lifting_unit
from bushidolib.parsing import parse_raw_unit, split_options
from bushidolib.unit import RawUnit
from bushidolib.wimhof import WimhofData, WimhofUnit, parse_wimhof_unit

UnitData = LiftingData | GymData | CardioData | WimhofData
UnitRepo = CardioUnitRepo | GymUnitRepo | LiftingUnitRepo | WimhofUnitRepo


def log_unit(line: str, session: Session) -> LoggedUnit:
    unit_settings = {
        setting.name: setting.category for setting in load_unit_settings(session)
    }
    raw_unit = parse_raw_unit(line)
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
) -> CardioUnit:
    repo = CardioUnitRepo(session)
    unit = CardioUnit(
        name=raw_unit.name,
        data=parse_cardio_unit(raw_unit.tokens),
        log_time=log_time,
        comment=raw_unit.comment,
    )
    repo.add_unit(unit)
    return unit


def log_gym_unit(
    raw_unit: RawUnit, log_time: datetime.datetime, session: Session
) -> GymUnit:
    repo = GymUnitRepo(session)
    unit = GymUnit(
        name=raw_unit.name,
        data=parse_gym_unit(raw_unit.tokens),
        log_time=log_time,
        comment=raw_unit.comment,
    )
    repo.add_unit(unit)
    return unit


def log_lifting_unit(
    raw_unit: RawUnit, log_time: datetime.datetime, session: Session
) -> LiftingUnit:
    repo = LiftingUnitRepo(session)
    unit = LiftingUnit(
        name=raw_unit.name,
        data=parse_lifting_unit(raw_unit.tokens),
        log_time=log_time,
        comment=raw_unit.comment,
    )
    repo.add_unit(unit)
    return unit


def log_wimhof_unit(
    raw_unit: RawUnit, log_time: datetime.datetime, session: Session
) -> WimhofUnit:
    repo = WimhofUnitRepo(session)
    unit = WimhofUnit(
        name=raw_unit.name,
        data=parse_wimhof_unit(raw_unit.tokens),
        log_time=log_time,
        comment=raw_unit.comment,
    )
    repo.add_unit(unit)
    return unit
