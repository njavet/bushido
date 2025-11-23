from bushido.infra.unit import UnitMapper
from bushido.modules.domain import UNIT_T, Err, Ok, Result
from bushido.modules.orm import UnitParser
from bushido.modules.repo import S, U, UnitRepo


def log_unit(line: str) -> Result[str]:
    unit_name, payload = line.split(" ", 1)


class LogUnitService:
    def __init__(
        self,
        parser: UnitParser[UNIT_T],
        mapper: UnitMapper[UNIT_T, U, S],
        repo: UnitRepo[U, S],
    ) -> None:
        self._parser = parser
        self._mapper = mapper
        self._repo = repo

    def log_unit(self, line: str) -> Result[str]:
        parse_result = self._parser.parse(line)
        if isinstance(parse_result, Err):
            return Err(parse_result.message)

        parsed_unit = parse_result.value
        unit, subunits = self._mapper.to_orm(parsed_unit)
        if self._repo.add_unit(unit, subunits):
            return Ok("Unit confirmed")
        else:
            return Err("error")
