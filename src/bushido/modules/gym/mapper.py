from typing import Any

from bushido.modules.dtypes import ParsedUnit, UnitMapper

from .domain import GymSpec
from .orm import GymUnit


class GymMapper(UnitMapper[GymSpec, GymUnit, Any]):
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[GymSpec]) -> tuple[GymUnit, list[Any]]:
        unit = GymUnit(name=parsed_unit.name, comment=parsed_unit.comment)
        return unit, []

    # TODO fix Any / None / []
    @staticmethod
    def from_orm(orms: tuple[GymUnit, list[Any]]) -> ParsedUnit[GymSpec]:
        unit, _ = orms
        pu = ParsedUnit(
            name=unit.name,
            data=GymSpec(
                start_t=unit.start_t,
                end_t=unit.end_t,
                location=unit.location,
                training=unit.training,
                focus=unit.focus,
            ),
            comment=unit.comment,
        )
        return pu
