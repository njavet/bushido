from dataclasses import dataclass
from typing import Any, Callable

from sqlalchemy.orm import Session

from bushido.unit.base import UnitMapper, UnitParser
from bushido.unit.repo import UnitRepo


RepoFactory = Callable[[Session], UnitRepo[Any]]


@dataclass(frozen=True, slots=True)
class UnitRegistration:
    parser: UnitParser[Any]
    mapper: UnitMapper[Any, Any]
    repo_factory: RepoFactory
    grammar: str

    def repo(self, session: Session) -> UnitRepo[Any]:
        return self.repo_factory(session)
