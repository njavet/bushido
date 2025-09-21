from dataclasses import dataclass
from typing import Generic, TypeVar

# project imports
from bushido.core.unit import UnitName


@dataclass
class UnitSpec:
    unit_name: str
    words: list[str]
    comment: str | None = None


T = TypeVar('T')


@dataclass
class ParsedUnit(Generic[T]):
    unit_name: UnitName
    data: T
    comment: str | None = None
