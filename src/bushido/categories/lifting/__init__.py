from bushido.core.dtypes import CategoryRegistration
from bushido.settings import LIFTING_UNIT_SETTINGS

from .mapper import LiftingMapper
from .parser import LiftingParser
from .repo import LiftingRepo

lifting_registration = CategoryRegistration(
    parser=LiftingParser(),
    mapper=LiftingMapper(),
    repo_factory=lambda session: LiftingRepo(session),
    grammar=LiftingParser.grammar,
    unit_settings=LIFTING_UNIT_SETTINGS,
)
