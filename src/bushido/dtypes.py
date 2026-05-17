import datetime
from dataclasses import dataclass
from typing import Any, Callable

from sqlalchemy.orm import Session

from bushido.conf import UnitType
from bushido.db.repo import UnitRepo
from bushido.protocols import UnitMapper, UnitParser


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
    unit_type: UnitType
    grammar: str
    emoji: str

    def repo(self, session: Session) -> UnitRepo[Any]:
        return self.repo_factory(session)
