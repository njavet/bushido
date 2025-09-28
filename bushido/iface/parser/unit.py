from typing import Protocol

from bushido.core.result import Result
from bushido.domain.unit import ParsedUnit, UnitSpec, UNIT_T


class UnitParser(Protocol[UNIT_T]):
    def parse(self, unit_spec: UnitSpec) -> Result[ParsedUnit[UNIT_T]]: ...
