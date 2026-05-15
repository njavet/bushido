import datetime
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

from sqlalchemy.orm import Session

from bushido.category.repo import UnitRepo
from bushido.category.protocols import UnitMapper, UnitParser


@dataclass(frozen=True, slots=True)
class SystemClock:
    timezone: datetime.tzinfo = datetime.UTC

    def now(self) -> datetime.datetime:
        return datetime.datetime.now(self.timezone)


@dataclass(frozen=True, slots=True)
class CategoryHelp:
    name: str
    grammar: str
    unit_names: list[str]


RepoFactory = Callable[[Session], UnitRepo[Any]]


@dataclass(frozen=True, slots=True)
class CategoryRegistration:
    parser: UnitParser[Any]
    mapper: UnitMapper[Any, Any]
    repo_factory: RepoFactory
    grammar: str
    unit_settings: dict[str, str]

    def repo(self, session: Session) -> UnitRepo[Any]:
        return self.repo_factory(session)


@dataclass(frozen=True, slots=True)
class TrainingUnit:
    name: str
    emoji: str
    date: datetime.datetime
    duration: int
    start_t: datetime.time | None = None
    end_t: datetime.time | None = None
    gym: str | None = None
    comment: str | None = None
