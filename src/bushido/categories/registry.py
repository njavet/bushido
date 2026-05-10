from .cardio import CardioMapper, CardioParser, CardioRepo
from .dtypes import CategoryHelp, CategoryRegistration
from .gym import GymMapper, GymParser, GymRepo
from .lifting import LiftingMapper, LiftingParser, LiftingRepo
from .unit_settings import (
    CARDIO_UNIT_SETTINGS,
    GYM_UNIT_SETTINGS,
    LIFTING_UNIT_SETTINGS,
    WIMHOF_UNIT_SETTINGS,
    UnitCategory,
)
from .wimhof import WimhofMapper, WimhofParser, WimhofRepo

REGISTRY: dict[str, CategoryRegistration] = {
    UnitCategory.gym: CategoryRegistration(
        parser=GymParser(),
        mapper=GymMapper(),
        repo_factory=GymRepo,
        grammar=GymParser.grammar,
        unit_settings=GYM_UNIT_SETTINGS,
    ),
    UnitCategory.lifting: CategoryRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        repo_factory=LiftingRepo,
        grammar=LiftingParser.grammar,
        unit_settings=LIFTING_UNIT_SETTINGS,
    ),
    UnitCategory.cardio: CategoryRegistration(
        parser=CardioParser(),
        mapper=CardioMapper(),
        repo_factory=CardioRepo,
        grammar=CardioParser.grammar,
        unit_settings=CARDIO_UNIT_SETTINGS,
    ),
    UnitCategory.wimhof: CategoryRegistration(
        parser=WimhofParser(),
        mapper=WimhofMapper(),
        repo_factory=WimhofRepo,
        grammar=WimhofParser.grammar,
        unit_settings=WIMHOF_UNIT_SETTINGS,
    ),
}


UNIT_TO_CATEGORY: dict[str, str] = {
    unit_name: category
    for category, registration in REGISTRY.items()
    for unit_name in registration.unit_settings.keys()
}


def get_category_help() -> list[CategoryHelp]:
    result = []
    for category, registration in REGISTRY.items():
        unit_names = [unit_name for unit_name in registration.unit_settings.keys()]
        ch = CategoryHelp(
            name=category, grammar=registration.grammar, unit_names=unit_names
        )
        result.append(ch)
    return result
