import datetime

from bushidolib.exceptions import UnitParsingError
from bushidolib.unit.base import BaseUnit, RawUnit
from sqlalchemy.orm import Session

from bushido_server.dtypes import Clock, SystemClock
from bushido_server.registry import UNIT_REGISTRY


def log_unit(line: str, session: Session) -> BaseUnit:
    raw_unit = RawUnit.from_line(line)
    override = raw_unit.options.get("dt", None)
    log_time = resolve_log_time(override=override, clock=SystemClock())

    try:
        spec = UNIT_REGISTRY[raw_unit.name]
    except KeyError as e:
        raise UnitParsingError(f"Unknown unit: {raw_unit.name}") from e

    repo = spec.repo(session)
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
