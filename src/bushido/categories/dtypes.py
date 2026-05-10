import datetime
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

from sqlalchemy.orm import Session

from bushido.categories.mapper import UnitMapper
from bushido.categories.orm import UnitTable
from bushido.categories.protocols import UnitParser
from bushido.categories.repo import UnitRepo


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


@dataclass(frozen=True, slots=True)
class RawUnit:
    name: str
    tokens: tuple[str, ...]
    comment: str | None = None


T = TypeVar("T")


@dataclass(frozen=True, slots=True)
class ParsedUnit(Generic[T]):
    name: str
    emoji: str
    data: T
    log_time: datetime.datetime
    comment: str | None = None


P = TypeVar("P", covariant=True)


@dataclass(frozen=True, slots=True)
class CategoryRegistration:
    parser: UnitParser[Any]
    mapper: UnitMapper[Any, Any]
    unit_cls: type[UnitTable]
    grammar: str
    unit_settings: dict[str, str]
    subrels: Any | None = None

    def repo(self, session: Session) -> UnitRepo[Any, Any]:
        if self.subrels is None:
            return UnitRepo(session=session, unit_cls=self.unit_cls)
        return UnitRepo(session=session, unit_cls=self.unit_cls, subrels=self.subrels)
