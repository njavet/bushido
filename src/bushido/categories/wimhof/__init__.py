from bushido.core.dtypes import CategoryRegistration
from bushido.settings import WIMHOF_UNIT_SETTINGS

from .mapper import WimhofMapper
from .parser import WimhofParser
from .repo import WimhofRepo

wimhof_registration = CategoryRegistration(
    parser=WimhofParser(),
    mapper=WimhofMapper(),
    repo_factory=lambda session: WimhofRepo(session),
    grammar=WimhofParser.grammar,
    unit_settings=WIMHOF_UNIT_SETTINGS,
)
