from typing import Protocol

from bushido.core.result import Result

# project imports
from bushido.core.types import UNIT_T
from bushido.domain.base import ParsedUnit, UnitSpec


class UnitParser(Protocol[UNIT_T]):
    def parse(self, unit_spec: UnitSpec) -> Result[ParsedUnit[UNIT_T]]: ...
