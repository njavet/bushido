from sqlalchemy.orm import selectinload

from bushido.adapter.mapper import CardioMapper, GymMapper, LiftingMapper, WimhofMapper
from bushido.dtypes import UnitRegistration
from bushido.persistence.models import (
    CardioUnitTable,
    GymUnitTable,
    LiftingUnitTable,
    WimhofUnitTable,
)
from bushido.persistence.repo import UnitRepo
from bushido.units.cardio import CardioParser, cardio_grammar, cardio_unit_settings
from bushido.units.gym import GymParser, gym_grammar, gym_unit_settings
from bushido.units.lifting import LiftingParser, lifting_grammar, lifting_unit_settings
from bushido.units.wimhof import WimhofParser, wimhof_grammar, wimhof_unit_settings


def build_registry() -> dict[str, UnitRegistration]:
    registry: dict[str, UnitRegistration] = {}
    for unit_setting in gym_unit_settings:
        registry[unit_setting.name] = UnitRegistration(
            parser=GymParser(),
            mapper=GymMapper(),
            repo_factory=lambda session: UnitRepo(session, GymUnitTable),
            grammar=gym_grammar,
            emoji=unit_setting.emoji,
        )
    for unit_setting in lifting_unit_settings:
        registry[unit_setting.name] = UnitRegistration(
            parser=LiftingParser(),
            mapper=LiftingMapper(),
            repo_factory=lambda session: UnitRepo(
                session,
                LiftingUnitTable,
                load_options=(selectinload(LiftingUnitTable.subunits),),
            ),
            grammar=lifting_grammar,
            emoji=unit_setting.emoji,
        )
    for unit_setting in wimhof_unit_settings:
        registry[unit_setting.name] = UnitRegistration(
            parser=WimhofParser(),
            mapper=WimhofMapper(),
            repo_factory=lambda session: UnitRepo(
                session,
                WimhofUnitTable,
                load_options=(selectinload(WimhofUnitTable.subunits),),
            ),
            grammar=wimhof_grammar,
            emoji=unit_setting.emoji,
        )
    for unit_setting in cardio_unit_settings:
        registry[unit_setting.name] = UnitRegistration(
            parser=CardioParser(),
            mapper=CardioMapper(),
            repo_factory=lambda session: UnitRepo(session, CardioUnitTable),
            grammar=cardio_grammar,
            emoji=unit_setting.emoji,
        )
    return registry
