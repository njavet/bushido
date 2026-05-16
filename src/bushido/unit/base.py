import datetime
from dataclasses import dataclass
from typing import Generic, TypeVar, Protocol

from bushido.unit.db_model import UnitTable

T = TypeVar("T")
P = TypeVar("P", covariant=True)
TU = TypeVar("TU", bound=UnitTable)


@dataclass(frozen=True, slots=True)
class RawUnit:
    name: str
    tokens: tuple[str, ...]
    comment: str | None = None


@dataclass(frozen=True, slots=True)
class Unit(Generic[T]):
    name: str
    emoji: str
    log_time: datetime.datetime
    comment: str | None
    data: T


class UnitParser(Protocol[P]):
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> P: ...


class UnitMapper(Protocol[T, TU]):
    @staticmethod
    def to_orm(unit: Unit[T]) -> TU: ...

    @staticmethod
    def from_orm(orm_unit: TU) -> Unit[T]: ...
