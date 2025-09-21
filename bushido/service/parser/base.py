from typing import Protocol

# project imports
from bushido.core.result import Result
from bushido.domain.base import UnitSpec, ParsedUnit


class UnitParser(Protocol):
    def parse(self, unit_spec: UnitSpec) -> Result[ParsedUnit]:
        ...

