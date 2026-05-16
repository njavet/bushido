import datetime
from dataclasses import dataclass
from typing import Any, Generic, Iterable, Protocol, TypeVar

from sqlalchemy.orm import Session

from bushido.units.db_model import UnitTable
from bushido.units.registry import RepoFactory
from bushido.units.repo import UnitRepo

T = TypeVar("T")
R = TypeVar("R")
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


@dataclass(frozen=True, slots=True)
class UnitRegistration:
    parser: UnitParser[Any]
    mapper: UnitMapper[Any, Any]
    repo_factory: RepoFactory
    grammar: str
    emoji: str

    def repo(self, session: Session) -> UnitRepo[Any]:
        return self.repo_factory(session)


class UnitMapper(Protocol[T, TU]):
    @staticmethod
    def to_orm(unit: Unit[T]) -> TU: ...

    @staticmethod
    def from_orm(orm_unit: TU) -> Unit[T]: ...


class UnitParser(Protocol[P]):
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> P: ...


class Metric(Protocol[T, R]):
    def compute(self, units: Iterable[Unit[T]]) -> R: ...
