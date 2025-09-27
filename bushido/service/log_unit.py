from bushido.core.result import Err, Ok, Result
from bushido.core.types import ORM_ST, ORM_T, UNIT_T
from bushido.domain.unit import UnitSpec
from bushido.iface.mapper.base import UnitMapper
from bushido.iface.parser.base import UnitParser
from bushido.infra.repo.base import UnitRepo


class LogUnitService:
    def __init__(
        self,
        repo: UnitRepo,
        parser: UnitParser[UNIT_T],
        mapper: UnitMapper[UNIT_T, ORM_T, ORM_ST],
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

    @staticmethod
    def preprocess_input(line: str) -> Result[UnitSpec]:
        parts = line.split('#', 1)
        payload = parts[0]

        if not payload:
            return Err('empty payload')
        if len(parts) > 1 and parts[1]:
            comment = parts[1].strip()
        else:
            comment = None
        all_words = payload.split()
        unit_name = all_words[0]
        words = all_words[1:]
        result = Ok(UnitSpec(name=unit_name, words=words, comment=comment))
        return result
