from bushido.adapter.mapper import CardioMapper, GymMapper, LiftingMapper, WimhofMapper
from bushido.dtypes import UnitRegistration
from bushido.units.cardio import CardioParser, cardio_grammar
from bushido.units.gym import GymParser, gym_grammar
from bushido.units.lifting import LiftingParser, lifting_grammar
from bushido.units.wimhof.grammar import grammar as wimhof_grammar
from bushido.units.wimhof.parser import WimhofParser

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
