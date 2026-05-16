import datetime
from typing import Protocol, TypeVar

from bushido.db.model.base import UnitTable
from bushido.units.base import Unit

TU = TypeVar("TU", bound=UnitTable)
T = TypeVar("T")
R = TypeVar("R", covariant=True)


class Clock(Protocol):
    def now(self) -> datetime.datetime: ...


class UnitParser(Protocol[R]):
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> R: ...


class UnitMapper(Protocol[T, TU]):
    @staticmethod
    def to_orm(unit: Unit[T]) -> TU: ...

    @staticmethod
    def from_orm(orm_unit: TU) -> Unit[T]: ...
