from typing import Protocol, TypeVar

from .dtypes import ParsedUnit
from .orm import Unit

T = TypeVar("T")
TU = TypeVar("TU", bound=Unit)


class UnitMapper(Protocol[T, TU]):
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[T]) -> TU: ...

    @staticmethod
    def from_orm(orm_unit: TU) -> ParsedUnit[T]: ...
