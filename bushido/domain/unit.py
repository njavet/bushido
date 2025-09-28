from dataclasses import dataclass
from typing import Generic, TypeVar


UNIT_T = TypeVar('UNIT_T')


@dataclass
class UnitSpec:
    name: str
    words: list[str]
    comment: str | None = None


@dataclass(frozen=True)
class ParsedUnit(Generic[UNIT_T]):
    name: str
    data: UNIT_T
    comment: str | None = None
