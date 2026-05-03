from typing import Protocol, TypeVar

from .orm import Subunit, Unit
from .parsing.base import ParsedUnit

T = TypeVar("T")
TU = TypeVar("TU", bound=Unit)
TS = TypeVar("TS", bound=Subunit)


class UnitMapper(Protocol[T, TU, TS]):
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[T]) -> tuple[TU, list[TS]]: ...

    @staticmethod
    def from_orm(orms: tuple[TU, list[TS]]) -> ParsedUnit[T]: ...
