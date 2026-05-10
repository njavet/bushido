from .cardio import CardioMapper, CardioParser, CardioUnitTable
from .dtypes import CategoryHelp, CategoryRegistration
from .gym import GymMapper, GymParser, GymUnitTable
from .lifting import LiftingMapper, LiftingParser, LiftingUnitTable
from .unit_settings import (
    CARDIO_UNIT_SETTINGS,
    GYM_UNIT_SETTINGS,
    LIFTING_UNIT_SETTINGS,
    WIMHOF_UNIT_SETTINGS,
    UnitCategory,
)
from .wimhof import WimhofMapper, WimhofParser, WimhofUnitTable

REGISTRY: dict[str, CategoryRegistration] = {
    UnitCategory.gym: CategoryRegistration(
        parser=GymParser(),
        mapper=GymMapper(),
        unit_cls=GymUnitTable,
        grammar=GymParser.grammar,
        unit_settings=GYM_UNIT_SETTINGS,
    ),
    UnitCategory.lifting: CategoryRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        unit_cls=LiftingUnitTable,
        grammar=LiftingParser.grammar,
        unit_settings=LIFTING_UNIT_SETTINGS,
        subrels=LiftingUnitTable.subunits,
    ),
    UnitCategory.cardio: CategoryRegistration(
        parser=CardioParser(),
        mapper=CardioMapper(),
        unit_cls=CardioUnitTable,
        grammar=CardioParser.grammar,
        unit_settings=CARDIO_UNIT_SETTINGS,
    ),
    UnitCategory.wimhof: CategoryRegistration(
        parser=WimhofParser(),
        mapper=WimhofMapper(),
        unit_cls=WimhofUnitTable,
        grammar=WimhofParser.grammar,
        unit_settings=WIMHOF_UNIT_SETTINGS,
        subrels=WimhofUnitTable.subunits,
    ),
}


UNIT_TO_CATEGORY: dict[str, str] = {
    unit_spec.name: category
    for category, registration in REGISTRY.items()
    for unit_spec in registration.unit_settings
}


def get_category_help() -> list[CategoryHelp]:
    result = []
    for category, registration in REGISTRY.items():
        unit_names = [unit_spec.name for unit_spec in registration.unit_settings]
        ch = CategoryHelp(
            name=category, grammar=registration.grammar, unit_names=unit_names
        )
        result.append(ch)
    return result
