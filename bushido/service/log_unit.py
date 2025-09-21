# project imports
from bushido.domain.unit import UnitSpec


class LogUnitService:
    def __init__(self):
        pass

    @staticmethod
    def preprocess_input(text: str) -> UnitSpec | None:
        parts = text.split('#', 1)
        payload = parts[0]
        if not payload:
            raise ValueError('Empty payload')
        if len(parts) > 1 and parts[1]:
            comment = parts[1].strip()
        else:
            comment = None
        all_words = payload.split()
        unit_name = all_words[0]
        words = all_words[1:]
        return UnitSpec(unit_name=unit_name,
                        words=words,
                        comment=comment)
