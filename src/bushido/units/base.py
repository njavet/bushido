import datetime
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from sqlalchemy.orm import Session

from bushido.units.db_model import UnitTable
from bushido.units.protocols import UnitMapper, UnitParser
from bushido.units.registry import RepoFactory
from bushido.units.repo import UnitRepo

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


@dataclass(frozen=True, slots=True)
class UnitRegistration:
    parser: UnitParser[Any]
    mapper: UnitMapper[Any, Any]
    repo_factory: RepoFactory
    grammar: str
    emoji: str

    def repo(self, session: Session) -> UnitRepo[Any]:
        return self.repo_factory(session)
