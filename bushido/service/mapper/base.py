from typing import Protocol

from annotated_types import Unit

# project imports
from bushido.core.result import Result
from bushido.domain.unit import ParsedUnit


class UnitMapper(Protocol):
    def to_orm(self, parsed_unit: ParsedUnit) -> Unit:
        ...
    def from_orm(self):
        ...

