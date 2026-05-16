from dataclasses import dataclass
from typing import Any, Callable

from sqlalchemy.orm import Session

from bushido.units.barbell.grammar import grammar as barbell_grammar
from bushido.units.barbell.mapper import BarbellMapper
from bushido.units.barbell.parser import BarbellParser
from bushido.units.barbell.repo import BarbellRepo
from bushido.units.base import UnitMapper, UnitParser
from bushido.units.repo import UnitRepo

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


UNIT_REGISTRY: dict[str, UnitRegistration] = {
    "squat": UnitRegistration(
        parser=BarbellParser(),
        mapper=BarbellMapper(),
        repo_factory=lambda session: BarbellRepo(session),
        grammar=barbell_grammar,
        emoji=b"\xe2\x9b\xa9\xef\xb8\x8f".decode(),
    ),
    "deadlift": UnitRegistration(
        parser=BarbellParser(),
        mapper=BarbellMapper(),
        repo_factory=lambda session: BarbellRepo(session),
        grammar=barbell_grammar,
        emoji=b"\xf0\x9f\x8f\x97\xef\xb8\x8f".decode(),
    ),
    "benchpress": UnitRegistration(
        parser=BarbellParser(),
        mapper=BarbellMapper(),
        repo_factory=lambda session: BarbellRepo(session),
        grammar=barbell_grammar,
        emoji=b"\xf0\x9f\x9b\xab".decode(),
    ),
    "overheadpress": UnitRegistration(
        parser=BarbellParser(),
        mapper=BarbellMapper(),
        repo_factory=lambda session: BarbellRepo(session),
        grammar=barbell_grammar,
        emoji=b"\xf0\x9f\x9a\x81".decode(),
    ),
    "rows": UnitRegistration(
        parser=BarbellParser(),
        mapper=BarbellMapper(),
        repo_factory=lambda session: BarbellRepo(session),
        grammar=barbell_grammar,
        emoji=b"\xf0\x9f\x90\xa2".decode(),
    ),
    "curls": UnitRegistration(
        parser=BarbellParser(),
        mapper=BarbellMapper(),
        repo_factory=lambda session: BarbellRepo(session),
        grammar=barbell_grammar,
        emoji=b"\xf0\x9f\xa6\xbe".decode(),
    ),
}
