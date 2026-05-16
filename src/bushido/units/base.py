import datetime
from dataclasses import dataclass
from typing import Any, Callable, Generic, Iterable, Protocol, TypeVar

from sqlalchemy.orm import Session

from bushido.db.repo import UnitRepo
from bushido.protocols import UnitMapper, UnitParser

T = TypeVar("T")
R = TypeVar("R", covariant=True)


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


RepoFactory = Callable[[Session], UnitRepo[Any]]


@dataclass(frozen=True, slots=True)
class UnitRegistration:
    parser: UnitParser[Any]
    mapper: UnitMapper[Any, Any]
    repo_factory: RepoFactory
    grammar: str
    emoji: str

    def repo(self, session: Session) -> UnitRepo[Any]:
        return self.repo_factory(session)


class UnitMetric(Protocol[T, R]):
    def compute(self, units: Iterable[Unit[T]]) -> R: ...
