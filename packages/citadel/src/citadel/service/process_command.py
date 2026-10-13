import datetime

from sqlalchemy.orm import Session

from citadel.bcl import dispatch_command
from citadel.bcl.parsers.log import LogUnitCommand
from citadel.dtypes import Clock, SystemClock
from citadel.exceptions import UnitParsingError
from citadel.persistence.models import Spartan
from citadel.registry import UNIT_REGISTRY
from citadel.schema.res import LoggedUnit


def process_command(line: str, session: Session, spartan: Spartan):
    preparsed_cmd = dispatch_command(line)


def log_unit(log_cmd: LogUnitCommand, session: Session, spartan: Spartan) -> LoggedUnit:
    override = log_cmd.options.get("dt", None)
    log_time = resolve_log_time(override=override, clock=SystemClock())

    try:
        spec = UNIT_REGISTRY[log_cmd.unit_name]
    except KeyError as e:
        raise UnitParsingError(f"Unknown unit: {log_cmd.unit_name}") from e

    repo = spec.repo(session)
    unit = spec.build_unit(log_cmd, log_time)
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
