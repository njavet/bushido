import datetime

from sqlalchemy.orm import Session

from bushido_server.dtypes import Clock, SystemClock
from bushido_server.registry import CATEGORY_REGISTRY
from bushido_server.settings import UNIT_NAME_REGISTRY
from bushidolib.exceptions import UnitParsingError
from bushidolib.schema.unit import BaseUnit, RawUnit


def log_unit(line: str, session: Session) -> BaseUnit:
    raw_unit = RawUnit.from_line(line)
    log_time = resolve_log_time(override=raw_unit.raw_log_time, clock=SystemClock())

    try:
        category = UNIT_NAME_REGISTRY[raw_unit.name]
    except KeyError as e:
        raise UnitParsingError(f"Unknown unit: {raw_unit.name}") from e

    try:
        spec = CATEGORY_REGISTRY[category]
    except KeyError as e:
        raise UnitParsingError(f"Unknown unit category: {category}") from e

    repo = spec.unit_repo(session)
    unit = spec.build_unit(raw_unit, log_time)
    repo.add_unit(unit)
    return unit


def resolve_log_time(override: str | None, clock: Clock) -> datetime.datetime:
    if override is None:
        return clock.now()
    # TODO handle user set timezone
    return datetime.datetime.strptime(override, "%Y%m%d-%H%M").replace(
        tzinfo=datetime.UTC
    )
