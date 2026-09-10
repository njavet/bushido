import datetime

from sqlalchemy.orm import Session

from bushido_server.dtypes import Clock, SystemClock
from bushido_server.registry import CATEGORY_REGISTRY
from bushido_server.settings import UNIT_NAME_REGISTRY
from bushidolib.category.base import (
    BaseUnit,
    parse_raw_unit,
    split_options,
)
from bushidolib.exceptions import UnitParsingError


def log_unit(line: str, session: Session) -> BaseUnit:
    raw_unit = parse_raw_unit(line)
    raw_unit.tokens, override = split_options(raw_unit.tokens)
    log_time = resolve_log_time(override, SystemClock)

    try:
        category = UNIT_NAME_REGISTRY[raw_unit.name]
    except KeyError:
        raise UnitParsingError(f"Unknown unit: {raw_unit.name}")

    try:
        spec = CATEGORY_REGISTRY[category]
    except KeyError:
        raise UnitParsingError(f"Unknown unit category: {category}")

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
