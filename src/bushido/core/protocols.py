import datetime
from typing import Protocol, TypeVar

from bushido.category.repo import TU


class Clock(Protocol):
    def now(self) -> datetime.datetime: ...


P = TypeVar("P", covariant=True)


class UnitParser(Protocol[P]):
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> P: ...


T = TypeVar("T")


class UnitMapper(Protocol[T, TU]):
    @staticmethod
    def to_orm(parsed_unit: T) -> TU: ...

    @staticmethod
    def from_orm(orm_unit: TU) -> T: ...
