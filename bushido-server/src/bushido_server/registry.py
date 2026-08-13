from bushido_server.persistence.repos import (
    CardioUnitRepo,
    GymUnitRepo,
    LiftingUnitRepo,
    WimhofUnitRepo,
)
from bushidolib.dtypes import UnitRegistration
from bushidolib.units.cardio import (
    CardioParser,
    cardio_grammar,
    cardio_unit_settings,
)
from bushidolib.units.gym import (
    GymParser,
    gym_grammar,
    gym_unit_settings,
)
from bushidolib.units.lifting import (
    LiftingParser,
    lifting_grammar,
    lifting_unit_settings,
)
from bushidolib.units.wimhof import (
    WimhofParser,
    wimhof_grammar,
    wimhof_unit_settings,
)


def build_registry() -> dict[str, UnitRegistration]:
    registry: dict[str, UnitRegistration] = {}
    for unit_setting in gym_unit_settings:
        registry[unit_setting.name] = UnitRegistration(
            parser=GymParser(),
            repo_factory=GymUnitRepo,
            grammar=gym_grammar,
            emoji=unit_setting.emoji,
        )
    for unit_setting in lifting_unit_settings:
        registry[unit_setting.name] = UnitRegistration(
            parser=LiftingParser(),
            repo_factory=LiftingUnitRepo,
            grammar=lifting_grammar,
            emoji=unit_setting.emoji,
        )
    for unit_setting in wimhof_unit_settings:
        registry[unit_setting.name] = UnitRegistration(
            parser=WimhofParser(),
            repo_factory=WimhofUnitRepo,
            grammar=wimhof_grammar,
            emoji=unit_setting.emoji,
        )
    for unit_setting in cardio_unit_settings:
        registry[unit_setting.name] = UnitRegistration(
            parser=CardioParser(),
            repo_factory=CardioUnitRepo,
            grammar=cardio_grammar,
            emoji=unit_setting.emoji,
        )
    return registry
