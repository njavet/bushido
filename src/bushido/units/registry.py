from bushido.units.base import UnitRegistration
from bushido.units.cardio.grammar import grammar as cardio_grammar
from bushido.units.cardio.mapper import CardioMapper
from bushido.units.cardio.parser import CardioParser
from bushido.units.cardio.repo import CardioRepo
from bushido.units.gym.grammar import grammar as gym_grammar
from bushido.units.gym.mapper import GymMapper
from bushido.units.gym.parser import GymParser
from bushido.units.gym.repo import GymRepo
from bushido.units.lifting.grammar import grammar as lifting_grammar
from bushido.units.lifting.mapper import LiftingMapper
from bushido.units.lifting.parser import LiftingParser
from bushido.units.lifting.repo import LiftingRepo
from bushido.units.wimhof.grammar import grammar as wimhof_grammar
from bushido.units.wimhof.mapper import WimhofMapper
from bushido.units.wimhof.parser import WimhofParser
from bushido.units.wimhof.repo import WimhofRepo

# TODO split
UNIT_REGISTRY: dict[str, UnitRegistration] = {
    "kyokushin": UnitRegistration(
        parser=GymParser(),
        mapper=GymMapper(),
        repo_factory=lambda session: GymRepo(session),
        grammar=gym_grammar,
        emoji=b"\xf0\x9f\xa5\x8b".decode(),
    ),
    "grappling": UnitRegistration(
        parser=GymParser(),
        mapper=GymMapper(),
        repo_factory=lambda session: GymRepo(session),
        grammar=gym_grammar,
        emoji=b"\xf0\x9f\xa5\x8b".decode(),
    ),
    "boxing": UnitRegistration(
        parser=GymParser(),
        mapper=GymMapper(),
        repo_factory=lambda session: GymRepo(session),
        grammar=gym_grammar,
        emoji=b"\xf0\x9f\xa5\x8b".decode(),
    ),
    "lifting": UnitRegistration(
        parser=GymParser(),
        mapper=GymMapper(),
        repo_factory=lambda session: GymRepo(session),
        grammar=gym_grammar,
        emoji=b"\xf0\x9f\xa6\x8d".decode(),
    ),
    "squat": UnitRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        repo_factory=lambda session: LiftingRepo(session),
        grammar=lifting_grammar,
        emoji=b"\xe2\x9b\xa9\xef\xb8\x8f".decode(),
    ),
    "deadlift": UnitRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        repo_factory=lambda session: LiftingRepo(session),
        grammar=lifting_grammar,
        emoji=b"\xf0\x9f\x8f\x97\xef\xb8\x8f".decode(),
    ),
    "benchpress": UnitRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        repo_factory=lambda session: LiftingRepo(session),
        grammar=lifting_grammar,
        emoji=b"\xf0\x9f\x9b\xab".decode(),
    ),
    "overheadpress": UnitRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        repo_factory=lambda session: LiftingRepo(session),
        grammar=lifting_grammar,
        emoji=b"\xf0\x9f\x9a\x81".decode(),
    ),
    "rows": UnitRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        repo_factory=lambda session: LiftingRepo(session),
        grammar=lifting_grammar,
        emoji=b"\xf0\x9f\x90\xa2".decode(),
    ),
    "curls": UnitRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        repo_factory=lambda session: LiftingRepo(session),
        grammar=lifting_grammar,
        emoji=b"\xf0\x9f\xa6\xbe".decode(),
    ),
    "wimhof": UnitRegistration(
        parser=WimhofParser(),
        mapper=WimhofMapper(),
        repo_factory=lambda session: WimhofRepo(session),
        grammar=wimhof_grammar,
        emoji=b"\xf0\x9f\xaa\x90".decode(),
    ),
    "running": UnitRegistration(
        parser=CardioParser(),
        mapper=CardioMapper(),
        repo_factory=lambda session: CardioRepo(session),
        grammar=cardio_grammar,
        emoji=b"\xf0\x9f\xaa\x96".decode(),
    ),
    "swimming": UnitRegistration(
        parser=CardioParser(),
        mapper=CardioMapper(),
        repo_factory=lambda session: CardioRepo(session),
        grammar=cardio_grammar,
        emoji=b"\xf0\x9f\xa6\x88".decode(),
    ),
    "skipping": UnitRegistration(
        parser=CardioParser(),
        mapper=CardioMapper(),
        repo_factory=lambda session: CardioRepo(session),
        grammar=cardio_grammar,
        emoji=b"\xf0\x9f\x8e\x97\xef\xb8\x8f".decode(),
    ),
}
