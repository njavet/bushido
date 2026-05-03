from typing import Any

from sqlalchemy.orm import Session

from bushido.core.dtypes import Clock, ParsedUnit, SystemClock
from bushido.core.result import Err, Ok, Result

# TODO rethink design
from bushido.units.factory import get_mapper, get_parser, get_repo, get_unit_names
from bushido.units.parsing.base import parse_raw_unit, split_options


class LogUnitService:
    def __init__(self, clock: Clock = SystemClock()) -> None:
        self.clock = clock
        self.unit_names = get_unit_names()

    def log_unit(self, line: str, session: Session) -> Result[ParsedUnit[Any]]:
        raw = parse_raw_unit(line)
        if raw.name not in self.unit_names:
            return Err(f"unit {raw.name} not found")

        tokens, log_time = split_options(raw.tokens, self.clock)

        # fetch log classes
        parser = get_parser(raw.name)
        mapper = get_mapper(raw.name)
        repo = get_repo(raw.name, session)

        # parse and store
        parse_res = parser.parse(tokens)
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

        unit, subunits = mapper.to_orm(parsed_unit)
        if repo.add_unit(unit, subunits):
            return Ok(parsed_unit)
        else:
            return Err("error")
