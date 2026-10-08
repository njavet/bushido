import datetime

from sqlalchemy.orm import Session

from citadel.dtypes import Clock, SystemClock
from citadel.exceptions import UnitParsingError
from citadel.persistence.models import Spartan
from citadel.registry import UNIT_REGISTRY
from citadel.unit.dtypes import LoggedUnit
from citadel.unit.base import RawUnit


def log_unit(line: str, session: Session, spartan: Spartan) -> LoggedUnit:
    raw_unit = RawUnit.from_line(line)
    override = raw_unit.options.get("dt", None)
    log_time = resolve_log_time(override=override, clock=SystemClock())

    try:
        spec = UNIT_REGISTRY[raw_unit.name]
    except KeyError as e:
        raise UnitParsingError(f"Unknown unit: {raw_unit.name}") from e

    repo = spec.repo(session)
    unit = spec.build_unit(raw_unit, log_time)
    repo.add_unit(unit, spartan.id)
    session.commit()
    return unit


def resolve_log_time(override: str | None, clock: Clock) -> datetime.datetime:
    if override is None:
        return clock.now()
    # TODO handle user set timezone
    return datetime.datetime.strptime(override, "%Y%m%d-%H%M").replace(
        tzinfo=datetime.UTC
    )
