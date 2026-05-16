from dataclasses import dataclass
from typing import Any, Callable

from sqlalchemy.orm import Session

from bushido.units.barbell.grammar import grammar as barbell_grammar
from bushido.units.barbell.mapper import BarbellMapper
from bushido.units.barbell.parser import BarbellParser
from bushido.units.barbell.repo import BarbellRepo
from bushido.units.base import UnitMapper, UnitParser
from bushido.units.lifting.grammar import grammar as lifting_grammar
from bushido.units.lifting.mapper import LiftingMapper
from bushido.units.lifting.parser import LiftingParser
from bushido.units.lifting.repo import LiftingRepo
from bushido.units.martial_arts.grammar import grammar as martial_arts_grammar
from bushido.units.martial_arts.mapper import MartialArtsMapper
from bushido.units.martial_arts.parser import MartialArtsParser
from bushido.units.martial_arts.repo import MartialArtsRepo
from bushido.units.repo import UnitRepo
from bushido.units.running.grammar import grammar as running_grammar
from bushido.units.running.mapper import RunningMapper
from bushido.units.running.parser import RunningParser
from bushido.units.running.repo import RunningRepo
from bushido.units.wimhof.grammar import grammar as wimhof_grammar
from bushido.units.wimhof.mapper import WimhofMapper
from bushido.units.wimhof.parser import WimhofParser
from bushido.units.wimhof.repo import WimhofRepo

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


# TODO split
UNIT_REGISTRY: dict[str, UnitRegistration] = {
    "kyokushin": UnitRegistration(
        parser=MartialArtsParser(),
        mapper=MartialArtsMapper(),
        repo_factory=lambda session: MartialArtsRepo(session),
        grammar=martial_arts_grammar,
        emoji=b"\xf0\x9f\xa5\x8b".decode(),
    ),
    "grappling": UnitRegistration(
        parser=MartialArtsParser(),
        mapper=MartialArtsMapper(),
        repo_factory=lambda session: MartialArtsRepo(session),
        grammar=martial_arts_grammar,
        emoji=b"\xf0\x9f\xa5\x8b".decode(),
    ),
    "boxing": UnitRegistration(
        parser=MartialArtsParser(),
        mapper=MartialArtsMapper(),
        repo_factory=lambda session: MartialArtsRepo(session),
        grammar=martial_arts_grammar,
        emoji=b"\xf0\x9f\xa5\x8b".decode(),
    ),
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
    "lifting": UnitRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        repo_factory=lambda session: LiftingRepo(session),
        grammar=lifting_grammar,
        emoji=b"\xf0\x9f\xa6\x8d".decode(),
    ),
    "wimhof": UnitRegistration(
        parser=WimhofParser(),
        mapper=WimhofMapper(),
        repo_factory=lambda session: WimhofRepo(session),
        grammar=wimhof_grammar,
        emoji=b"\xf0\x9f\xaa\x90".decode(),
    ),
    "running": UnitRegistration(
        parser=RunningParser(),
        mapper=RunningMapper(),
        repo_factory=lambda session: RunningRepo(session),
        grammar=running_grammar,
        emoji=b"\xf0\x9f\xaa\x96".decode(),
    ),
}
