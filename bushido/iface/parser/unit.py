from typing import Protocol

from bushido.core.result import Result
from bushido.domain.unit import UNIT_T, ParsedUnit, UnitSpec


class UnitParser(Protocol[UNIT_T]):
    def parse(self, unit_spec: UnitSpec) -> Result[ParsedUnit[UNIT_T]]: ...
