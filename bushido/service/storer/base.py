from typing import Protocol

# project imports
from bushido.core.result import Result
from bushido.domain.unit import ParsedUnit


class UnitStorer(Protocol):
    def store(self, parsed_unit: ParsedUnit) -> Result[int]:
        ...
