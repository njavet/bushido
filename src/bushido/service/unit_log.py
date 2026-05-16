import datetime
from typing import Any

from sqlalchemy.orm import Session

from bushido.unit.base import RawUnit, Unit
from bushido.unit.dt_parse import parse_datetime
from bushido.unit.exceptions import ParsingError
from bushido.dtypes import SystemClock
from bushido.protocols import Clock

from bushido.unit.registry import UNIT_REGISTRY, Registry


class UnitLogService:
    def __init__(self, registry: dict[str, Registry] = UNIT_REGISTRY, clock: Clock = SystemClock()) -> None:
        self.registry = registry
        self.clock = clock

    def log_unit(self, line: str, session: Session) -> None:
        raw = parse_raw_unit(line)
        try:
            unit_registry = self.registry[raw.name]
        except KeyError:
            raise ParsingError(f"Unknown unit {raw.name}")

        tokens, log_time_str = split_options(raw.tokens)
        if log_time_str:
            log_time = parse_datetime(log_time_str)
        else:
            log_time = self.clock.now()

        unit_data = unit_registry.parser.parse(tokens)

        parsed_unit = Unit(
            name=raw.name,
            emoji=unit_registry.unit_settings[raw.name],
            data=unit_data,
            log_time=log_time,
            comment=raw.comment,
        )
        unit = unit_registry.mapper.to_orm(parsed_unit)
        unit_registry.repo(session).add_unit(unit)


def parse_raw_unit(line: str) -> RawUnit:
    body, sep, comment = line.partition("#")
    tokens = tuple(body.split())

    if not tokens:
        raise ParsingError(f"Empty unit line: {line}")

    return RawUnit(
        name=tokens[0],
        tokens=tokens[1:],
        comment=comment.strip() if sep and comment.strip() else None,
    )


def split_options(tokens: tuple[str, ...]) -> tuple[tuple[str, ...], str | None]:
    clean: list[str] = []
    log_time: str | None = None
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token == "--dt":
            if i + 1 >= len(tokens):
                raise ParsingError("--dt requires a value")
            log_time = tokens[i + 1]
            i += 2
            continue
        clean.append(token)
        i += 1
    return tuple(clean), log_time
