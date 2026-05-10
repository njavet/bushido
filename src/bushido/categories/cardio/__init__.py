from bushido.core.dtypes import CategoryRegistration
from bushido.settings import CARDIO_UNIT_SETTINGS

from .mapper import CardioMapper
from .parser import CardioParser
from .repo import CardioRepo

cardio_registration = CategoryRegistration(
    parser=CardioParser(),
    mapper=CardioMapper(),
    repo_factory=lambda session: CardioRepo(session),
    grammar=CardioParser.grammar,
    unit_settings=CARDIO_UNIT_SETTINGS,
)
