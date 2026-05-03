from dataclasses import dataclass
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
from bushido.units.units import UnitCategory
from bushido.units.wimhof import (
    WimhofMapper,
    WimhofParser,
    WimhofUnit,
)


@dataclass(frozen=True, slots=True)
class UnitRegistration:
    parser: UnitParser[Any]
    mapper: UnitMapper[Any, Any, Any]
    unit_cls: Any
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
        grammar=GymParser.grammar,
    ),
    UnitCategory.lifting: UnitRegistration(
        parser=LiftingParser(),
        mapper=LiftingMapper(),
        unit_cls=LiftingUnit,
        grammar=LiftingParser.grammar,
        subrels=LiftingUnit.subunits,
    ),
    UnitCategory.cardio: UnitRegistration(
        parser=CardioParser(),
        mapper=CardioMapper(),
        unit_cls=CardioUnit,
        grammar=LiftingParser.grammar,
    ),
    UnitCategory.wimhof: UnitRegistration(
        parser=WimhofParser(),
        mapper=WimhofMapper(),
        unit_cls=WimhofUnit,
        grammar=WimhofParser.grammar,
        subrels=WimhofUnit.subunits,
    ),
}
