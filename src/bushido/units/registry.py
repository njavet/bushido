from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from sqlalchemy.orm import Session

from bushido.units.cardio import CardioMapper, CardioParser, CardioUnit, CardioUnitName
from bushido.units.gym import GymMapper, GymParser, GymUnit, GymUnitName
from bushido.units.lifting import (
    LiftingMapper,
    LiftingParser,
    LiftingUnit,
    LiftingUnitName,
)
from bushido.units.mapper import UnitMapper
from bushido.units.parsing.base import UnitParser
from bushido.units.repo import UnitRepo
from bushido.units.wimhof import (
    WimhofMapper,
    WimhofParser,
    WimhofUnit,
    WimhofUnitName,
)
from bushido.units.work import WorkUnitName


class UnitCategory(StrEnum):
    cardio = "cardio"
    lifting = "lifting"
    work = "work"
    gym = "gym"
    wimhof = "wimhof"


def unit_name_to_category(unit_name: str) -> UnitCategory:
    if unit_name in GymUnitName:
        return UnitCategory.gym
    elif unit_name in LiftingUnitName:
        return UnitCategory.lifting
    elif unit_name in WimhofUnitName:
        return UnitCategory.wimhof
    elif unit_name in CardioUnitName:
        return UnitCategory.cardio
    elif unit_name in WorkUnitName:
        return UnitCategory.work
    else:
        raise ValueError(f"Unknown unit: {unit_name}")


@dataclass(frozen=True, slots=True)
class UnitRegistration:
    parser: UnitParser[Any]
    mapper: UnitMapper[Any, Any, Any]
    unit_cls: Any
    unit_names: Any
    grammar: str
    subrels: Any | None = None

    def repo(self, session: Session) -> UnitRepo[Any, Any]:
        if self.subrels is None:
            return UnitRepo(session=session, unit_cls=self.unit_cls)
        return UnitRepo(session=session, unit_cls=self.unit_cls, subrels=self.subrels)


REGISTRY: dict[str, UnitRegistration] = {
    UnitCategory.gym: UnitRegistration(
        parser=GymParser(),
        mapper=GymMapper(),
        unit_cls=GymUnit,
        unit_names=GymUnitName,
        grammar=GymParser.grammar,
    ),
    UnitCategory.lifting: UnitRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        unit_cls=LiftingUnit,
        unit_names=LiftingUnitName,
        grammar=LiftingParser.grammar,
        subrels=LiftingUnit.subunits,
    ),
    UnitCategory.cardio: UnitRegistration(
        parser=CardioParser(),
        mapper=CardioMapper(),
        unit_cls=CardioUnit,
        unit_names=CardioUnitName,
        grammar=LiftingParser.grammar,
    ),
    UnitCategory.wimhof: UnitRegistration(
        parser=WimhofParser(),
        mapper=WimhofMapper(),
        unit_cls=WimhofUnit,
        unit_names=WimhofUnitName,
        grammar=WimhofParser.grammar,
        subrels=WimhofUnit.subunits,
    ),
}
