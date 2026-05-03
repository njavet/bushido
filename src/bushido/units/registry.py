from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from sqlalchemy.orm import Session

from bushido.units.cardio import CardioMapper, CardioParser, CardioUnit
from bushido.units.gym import GymMapper, GymParser, GymUnit
from bushido.units.lifting import (
    LiftingMapper,
    LiftingParser,
    LiftingUnit,
)
from bushido.units.mapper import UnitMapper
from bushido.units.parsing.base import UnitParser
from bushido.units.repo import UnitRepo
from bushido.units.wimhof import (
    WimhofMapper,
    WimhofParser,
    WimhofUnit,
)


class UnitCategory(StrEnum):
    cardio = "cardio"
    lifting = "lifting"
    work = "work"
    gym = "gym"
    wimhof = "wimhof"


@dataclass(frozen=True, slots=True)
class CategoryRegistration:
    parser: UnitParser[Any]
    mapper: UnitMapper[Any, Any, Any]
    unit_cls: Any
    grammar: str
    unit_names: list[str]
    subrels: Any | None = None

    def repo(self, session: Session) -> UnitRepo[Any, Any]:
        if self.subrels is None:
            return UnitRepo(session=session, unit_cls=self.unit_cls)
        return UnitRepo(session=session, unit_cls=self.unit_cls, subrels=self.subrels)


REGISTRY: dict[str, CategoryRegistration] = {
    UnitCategory.gym: CategoryRegistration(
        parser=GymParser(),
        mapper=GymMapper(),
        unit_cls=GymUnit,
        grammar=GymParser.grammar,
        unit_names=GymParser.unit_names,
    ),
    UnitCategory.lifting: CategoryRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        unit_cls=LiftingUnit,
        grammar=LiftingParser.grammar,
        unit_names=LiftingParser.unit_names,
        subrels=LiftingUnit.subunits,
    ),
    UnitCategory.cardio: CategoryRegistration(
        parser=CardioParser(),
        mapper=CardioMapper(),
        unit_cls=CardioUnit,
        grammar=LiftingParser.grammar,
        unit_names=CardioParser.unit_names,
    ),
    UnitCategory.wimhof: CategoryRegistration(
        parser=WimhofParser(),
        mapper=WimhofMapper(),
        unit_cls=WimhofUnit,
        grammar=WimhofParser.grammar,
        unit_names=WimhofParser.unit_names,
        subrels=WimhofUnit.subunits,
    ),
}


UNIT_TO_CATEGORY: dict[str, str] = {
    unit_name: category
    for category, registration in REGISTRY.items()
    for unit_name in registration.unit_names
}


def get_unit_names() -> list[str]:
    return sorted(UNIT_TO_CATEGORY)
