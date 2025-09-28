from bushido.core.result import Err, Ok, Result
from bushido.domain.unit import UnitSpec, UNIT_T
from bushido.iface.mapper.unit import UnitMapper
from bushido.iface.parser.unit import UnitParser
from bushido.infra.repo.unit import UnitRepo


class LogUnitService:
    def __init__(
        self,
        repo: UnitRepo,
        parser: UnitParser,
        mapper: UnitMapper
    ) -> None:
        self._repo = repo
        self._parser = parser
        self._mapper = mapper

    def log_unit(self, line: str) -> Result[str]:
        pre_result = self.preprocess_input(line)
        if isinstance(pre_result, Err):
            return pre_result

        unit_spec = pre_result.value
        parse_result = self._parser.parse(unit_spec)
        if isinstance(parse_result, Err):
            return parse_result

        parsed_unit = parse_result.value
        unit, subunits = self._mapper.to_orm(parsed_unit)
        if self._repo.add_unit(unit, subunits):
            return Ok('Unit confirmed')
        else:
            return Err('db error')

