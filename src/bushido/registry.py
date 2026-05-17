from bushido.domain.units import (
    CardioParser,
    GymParser,
    LiftingParser,
    cardio_grammar,
    cardio_unit_settings,
    gym_grammar,
    gym_unit_settings,
    lifting_grammar,
    lifting_unit_settings,
)
from bushido.domain.units.wimhof import (
    WimhofParser,
    wimhof_grammar,
    wimhof_unit_settings,
)
from bushido.dtypes import UnitRegistration
from bushido.persistence.repos import (
    CardioUnitRepo,
    GymUnitRepo,
    LiftingUnitRepo,
    WimhofUnitRepo,
)


def build_registry() -> dict[str, UnitRegistration]:
    registry: dict[str, UnitRegistration] = {}
    for unit_setting in gym_unit_settings:
        registry[unit_setting.name] = UnitRegistration(
            parser=GymParser(),
            repo_factory=lambda session: GymUnitRepo(session),
            grammar=gym_grammar,
            emoji=unit_setting.emoji,
        )
    for unit_setting in lifting_unit_settings:
        registry[unit_setting.name] = UnitRegistration(
            parser=LiftingParser(),
            repo_factory=lambda session: LiftingUnitRepo(session),
            grammar=lifting_grammar,
            emoji=unit_setting.emoji,
        )
    for unit_setting in wimhof_unit_settings:
        registry[unit_setting.name] = UnitRegistration(
            parser=WimhofParser(),
            repo_factory=lambda session: WimhofUnitRepo(session),
            grammar=wimhof_grammar,
            emoji=unit_setting.emoji,
        )
    for unit_setting in cardio_unit_settings:
        registry[unit_setting.name] = UnitRegistration(
            parser=CardioParser(),
            repo_factory=lambda session: CardioUnitRepo(session),
            grammar=cardio_grammar,
            emoji=unit_setting.emoji,
        )
    return registry
