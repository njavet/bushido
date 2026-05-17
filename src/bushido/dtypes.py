import datetime
from dataclasses import dataclass
from typing import Any, Callable, Iterable, Protocol, TypeVar

from sqlalchemy.orm import Session

from bushido.db.repo import T_ORM, UnitRepo
from bushido.units import Unit

T = TypeVar("T")
R = TypeVar("R", covariant=True)


@dataclass(frozen=True, slots=True)
class SystemClock:
    timezone: datetime.tzinfo = datetime.UTC

    def now(self) -> datetime.datetime:
        return datetime.datetime.now(self.timezone)


@dataclass(frozen=True, slots=True)
class UnitRegistration:
    parser: UnitParser[Any]
    mapper: UnitMapper[Any, Any]
    repo_factory: Callable[[Session], UnitRepo[Any]]
    grammar: str
    emoji: str

    def repo(self, session: Session) -> UnitRepo[Any]:
        return self.repo_factory(session)


class UnitMetric(Protocol[T, R]):
    def compute(self, units: Iterable[Unit[T]]) -> R: ...


class UnitMapper(Protocol[T, T_ORM]):
    @staticmethod
    def to_orm(unit: Unit[T]) -> T_ORM: ...

    @staticmethod
    def from_orm(orm_unit: T_ORM) -> Unit[T]: ...


class UnitParser(Protocol[R]):
    @staticmethod
    def parse(tokens: tuple[str, ...]) -> R: ...


class Clock(Protocol):
    def now(self) -> datetime.datetime: ...
