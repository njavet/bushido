# project imports
from bushido.core.result import Result, Err, Ok
from bushido.domain.unit import UnitSpec


class LogUnitService:
    def __init__(self):
        pass

    def log_unit(self, line: str) -> Result[str]:
        pre_result = self.preprocess_input(line)
        if isinstance(pre_result, Err):
            result = Err(pre_result.message)
        else:
            unit_spec = pre_result.value


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
