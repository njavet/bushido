from bushido.core.dtypes import CategoryRegistration
from bushido.settings import GYM_UNIT_SETTINGS

from .mapper import GymMapper
from .parser import GymParser
from .repo import GymRepo

gym_registration = CategoryRegistration(
    parser=GymParser(),
    mapper=GymMapper(),
    repo_factory=lambda session: GymRepo(session),
    grammar=GymParser.grammar,
    unit_settings=GYM_UNIT_SETTINGS,
)
