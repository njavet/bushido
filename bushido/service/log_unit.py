from bushido.core.result import Err, Ok, Result
from bushido.core.types import UNIT_T, ORM_T, ORM_ST
from bushido.domain.base import UnitSpec
from bushido.repo.base import UnitRepo
from bushido.service.mapper.base import UnitMapper
from bushido.service.parser.base import UnitParser


class LogUnitService:
    def __init__(
        self, repo: UnitRepo, parser: UnitParser[UNIT_T], mapper: UnitMapper[UNIT_T, ORM_T, ORM_ST]
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

        if payload:
            if len(parts) > 1 and parts[1]:
                comment = parts[1].strip()
            else:
                comment = None
            all_words = payload.split()
            unit_name = all_words[0]
            words = all_words[1:]
            result = Ok(
                UnitSpec(unit_name=unit_name, words=words, comment=comment)
            )
        else:
            result = Err('empty payload')
        return result
