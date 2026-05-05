from typing import Protocol, TypeVar

from .dtypes import ParsedUnit
from .repo import TU

T = TypeVar("T")


class UnitMapper(Protocol[T, TU]):
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[T]) -> TU: ...

    @staticmethod
    def from_orm(orm_unit: TU) -> ParsedUnit[T]: ...
