from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from sqlalchemy.orm import Session

from bushido.core.dtypes import Clock, SystemClock
from bushido.core.result import Err, Ok, Result
from bushido.units import (
    REGISTRY,
    UNIT_TO_CATEGORY,
    ParsedUnit,
    get_unit_names,
    parse_raw_unit,
    split_options,
)


@dataclass(frozen=True, slots=True)
class UnitHelp:
    grammar: str
    unit_names: StrEnum


class LogUnitService:
    def __init__(self, clock: Clock = SystemClock()) -> None:
        self.clock = clock
        self.registry = REGISTRY

    def log_unit(self, line: str, session: Session) -> Result[ParsedUnit[Any]]:
        raw = parse_raw_unit(line)
        try:
            category = UNIT_TO_CATEGORY[raw.name]
        except KeyError:
            return Err("unknown unit")
        registry = self.registry[category]
        tokens, log_time = split_options(raw.tokens, self.clock)

        parse_res = registry.parser.parse(tokens)
        if isinstance(parse_res, Err):
            return parse_res
        else:
            unit_data = parse_res.value

        parsed_unit = ParsedUnit(
            name=raw.name,
            data=unit_data,
            log_time=log_time,
            comment=raw.comment,
        )
        unit, subunits = registry.mapper.to_orm(parsed_unit)
        if registry.repo(session).add_unit(unit, subunits):
            return Ok(parsed_unit)
        else:
            return Err("error")

    @property
    def unit_names(self) -> list[str]:
        return get_unit_names()
