from typing import Any

from sqlalchemy.orm import Session

from bushido.core.dtypes import ParsedUnit
from bushido.core.result import Err, Ok, Result

# TODO rethink design
from bushido.modules.factory import get_mapper, get_parser, get_repo, get_unit_names


class LogUnitService:
    @staticmethod
    def log_unit(line: str, session: Session) -> Result[ParsedUnit[Any]]:
        try:
            unit_name, payload = line.split(" ", 1)
        except ValueError:
            unit_name, payload = line, ""

        if unit_name not in get_unit_names():
            return Err(f"unit {unit_name} not found")

        # fetch log classes
        parser = get_parser(unit_name)
        mapper = get_mapper(unit_name)
        repo = get_repo(unit_name, session)

        # parse and store
        parse_res = parser.parse(payload)
        if isinstance(parse_res, Err):
            return parse_res
        else:
            parsed_unit = parse_res.value

        unit, subunits = mapper.to_orm(parsed_unit)
        if repo.add_unit(unit, subunits):
            return Ok(parsed_unit)
        else:
            return Err("error")
