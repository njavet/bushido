from dataclasses import dataclass
from typing import Generic

# project imports
from bushido.core.types import UNIT_T
from bushido.core.unit import UnitName


@dataclass
class UnitSpec:
    unit_name: str
    words: list[str]
    comment: str | None = None


@dataclass
class ParsedUnit(Generic[UNIT_T]):
    unit_name: UnitName
    data: UNIT_T
    comment: str | None = None
