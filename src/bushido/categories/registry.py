from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from .cardio import CardioMapper, CardioParser, CardioUnitTable
from .dtypes import CategoryHelp, UnitParser
from .gym import GymMapper, GymParser, GymUnitTable
from .lifting import LiftingMapper, LiftingParser, LiftingUnitTable
from .mapper import UnitMapper
from .orm import UnitTable
from .repo import UnitRepo
from .unit_settings import (
    CardioUnitName,
    GymUnitName,
    LiftingUnitName,
    UnitCategory,
    WimhofUnitName,
)
from .wimhof import WimhofMapper, WimhofParser, WimhofUnitTable


@dataclass(frozen=True, slots=True)
class CategoryRegistration:
    parser: UnitParser[Any]
    mapper: UnitMapper[Any, Any]
    unit_cls: type[UnitTable]
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
        unit_cls=GymUnitTable,
        grammar=GymParser.grammar,
        unit_names=[x.name for x in GymUnitName],
    ),
    UnitCategory.lifting: CategoryRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        unit_cls=LiftingUnitTable,
        grammar=LiftingParser.grammar,
        unit_names=[x.name for x in LiftingUnitName],
        subrels=LiftingUnitTable.subunits,
    ),
    UnitCategory.cardio: CategoryRegistration(
        parser=CardioParser(),
        mapper=CardioMapper(),
        unit_cls=CardioUnitTable,
        grammar=CardioParser.grammar,
        unit_names=[x.name for x in CardioUnitName],
    ),
    UnitCategory.wimhof: CategoryRegistration(
        parser=WimhofParser(),
        mapper=WimhofMapper(),
        unit_cls=WimhofUnitTable,
        grammar=WimhofParser.grammar,
        unit_names=[x.name for x in WimhofUnitName],
        subrels=WimhofUnitTable.subunits,
    ),
}


UNIT_TO_CATEGORY: dict[str, str] = {
    unit_name: category
    for category, registration in REGISTRY.items()
    for unit_name in registration.unit_names
}


def get_category_help() -> list[CategoryHelp]:
    return [
        CategoryHelp(name=category, grammar=r.grammar, unit_names=r.unit_names)
        for category, r in REGISTRY.items()
    ]
