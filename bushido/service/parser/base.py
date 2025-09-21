from typing import Protocol

# project imports
from bushido.core.types import UNIT_T
from bushido.core.result import Result
from bushido.domain.base import ParsedUnit, UnitSpec



class UnitParser(Protocol):
    def parse(self, unit_spec: UnitSpec) -> Result[ParsedUnit[UNIT_T]]: ...
