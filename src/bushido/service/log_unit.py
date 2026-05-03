from typing import Any

from sqlalchemy.orm import Session

from bushido.core.dtypes import Clock, ParsedUnit, SystemClock
from bushido.core.result import Err, Ok, Result
from bushido.units.parsing.base import parse_raw_unit, split_options
from bushido.units.units import get_registration


class LogUnitService:
    def __init__(self, clock: Clock = SystemClock()) -> None:
        self.clock = clock

    def log_unit(self, line: str, session: Session) -> Result[ParsedUnit[Any]]:
        raw = parse_raw_unit(line)
        registry = get_registration(raw.name)

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
