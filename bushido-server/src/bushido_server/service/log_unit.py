import datetime

from bushidolib.category.base.unit import (
    RawUnit,
    build_unit,
    parse_raw_unit,
    split_options,
)
from sqlalchemy.orm import Session

from bushido_server.dtypes import Clock, SystemClock
from bushido_server.persistence.repos import (
    CardioUnitRepo,
    GymUnitRepo,
    LiftingUnitRepo,
    WimhofUnitRepo,
)
from bushido_server.settings import UNIT_NAME_REGISTRY
from bushidolib.category.cardio import CardioData, CardioUnit, parse_cardio_unit
from bushidolib.category.gym import GymData, GymUnit, parse_gym_unit
from bushidolib.category.lifting import LiftingData, LiftingUnit, parse_lifting_unit
from bushidolib.category.wimhof import WimhofData, WimhofUnit, parse_wimhof_unit
from bushidolib.exceptions import UnitParsingError

UnitData = LiftingData | GymData | CardioData | WimhofData
UnitRepo = CardioUnitRepo | GymUnitRepo | LiftingUnitRepo | WimhofUnitRepo


def log_unit(line: str, session: Session) -> LoggedUnit:
    raw_unit = parse_raw_unit(line)
    raw_unit.tokens, override = split_options(raw_unit.tokens)
    log_time = resolve_log_time(override, SystemClock)

    try:
        category = UNIT_NAME_REGISTRY[raw_unit.name]
    except KeyError:
        raise UnitParsingError(f"Unknown unit: {raw_unit.name}")

    unit = build_unit(raw_unit, category, log_time)


def resolve_log_time(override: str | None, clock: Clock) -> datetime.datetime:
    if override is None:
        return clock.now()
    # TODO handle user set timezone
    return datetime.datetime.strptime(override, "%Y%m%d-%H%M").replace(
        tzinfo=datetime.UTC
    )


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
