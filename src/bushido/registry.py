from sqlalchemy.orm import selectinload

from bushido.adapter.mapper import CardioMapper, GymMapper, LiftingMapper, WimhofMapper
from bushido.conf import UnitType
from bushido.db.model import (
    CardioUnitTable,
    GymUnitTable,
    LiftingUnitTable,
    WimhofUnitTable,
)
from bushido.db.repo import UnitRepo
from bushido.dtypes import UnitRegistration
from bushido.settings import UnitSetting
from bushido.units.cardio import CardioParser, cardio_grammar
from bushido.units.gym import GymParser, gym_grammar
from bushido.units.lifting import LiftingParser, lifting_grammar
from bushido.units.wimhof import WimhofParser, wimhof_grammar


def build_registry(unit_settings: list[UnitSetting]) -> dict[str, UnitRegistration]:
    registry: dict[str, UnitRegistration] = {}
    for unit_setting in unit_settings:
        match unit_setting.unit_type:
            case UnitType.GYM:
                registry[unit_setting.name] = UnitRegistration(
                    parser=GymParser(),
                    mapper=GymMapper(),
                    repo_factory=lambda session: UnitRepo(session, GymUnitTable),
                    unit_type=UnitType.GYM,
                    grammar=gym_grammar,
                    emoji=unit_setting.emoji,
                )
            case UnitType.LIFTING:
                registry[unit_setting.name] = UnitRegistration(
                    parser=LiftingParser(),
                    mapper=LiftingMapper(),
                    repo_factory=lambda session: UnitRepo(
                        session,
                        LiftingUnitTable,
                        load_options=(selectinload(LiftingUnitTable.subunits),),
                    ),
                    unit_type=UnitType.LIFTING,
                    grammar=lifting_grammar,
                    emoji=unit_setting.emoji,
                )
            case UnitType.WIMHOF:
                registry[unit_setting.name] = UnitRegistration(
                    parser=WimhofParser(),
                    mapper=WimhofMapper(),
                    repo_factory=lambda session: UnitRepo(
                        session,
                        WimhofUnitTable,
                        load_options=(selectinload(WimhofUnitTable.subunits),),
                    ),
                    unit_type=UnitType.WIMHOF,
                    grammar=wimhof_grammar,
                    emoji=unit_setting.emoji,
                )
            case UnitType.CARDIO:
                registry[unit_setting.name] = UnitRegistration(
                    parser=CardioParser(),
                    mapper=CardioMapper(),
                    repo_factory=lambda session: UnitRepo(session, CardioUnitTable),
                    unit_type=UnitType.CARDIO,
                    grammar=cardio_grammar,
                    emoji=unit_setting.emoji,
                )
            case _:
                raise ValueError(f"unknown unit type {unit_setting.unit_type}")
    return registry
