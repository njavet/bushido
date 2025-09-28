from bushido.core.result import Err, Ok, Result
from bushido.domain.unit import UNIT_T
from bushido.iface.mapper.unit import UnitMapper
from bushido.iface.parser.unit import UnitParser
from bushido.iface.parser.utils import preprocess_input
from bushido.infra.repo.unit import S, U, UnitRepo


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
        pre_result = preprocess_input(line)
        if isinstance(pre_result, Err):
            return Err('preprocess error')

        unit_spec = pre_result.value
        parse_result = self._parser.parse(unit_spec)
        if isinstance(parse_result, Err):
            return Err('parse error')

        parsed_unit = parse_result.value
        unit, subunits = self._mapper.to_orm(parsed_unit)
        if self._repo.add_unit(unit, subunits):
            return Ok('success')
        else:
            return Err('error')
