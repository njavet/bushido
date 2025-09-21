# project imports
from bushido.core.result import Result, Err, Ok
from bushido.domain.unit import UnitSpec
from bushido.service.parser.base import UnitParser
from bushido.service.mapper.base import UnitMapper
from bushido.service.storer.base import UnitStorer


class LogUnitService:
    def __init__(self, parser: UnitParser, mapper: UnitMapper, storer: UnitStorer) -> None:
        self._parser = parser
        self._mapper = mapper
        self._storer = storer

    def log_unit(self, line: str) -> Result[str]:
        pre_result = self.preprocess_input(line)
        if isinstance(pre_result, Ok):
            unit_spec = pre_result.value

        else:
            result = Err(pre_result.message)

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
            result = Ok(UnitSpec(unit_name=unit_name,
                                 words=words,
                                 comment=comment))
        else:
            result = Err('empty payload')
        return result
