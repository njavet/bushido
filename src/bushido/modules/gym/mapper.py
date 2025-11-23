from typing import Any

from bushido.modules.domain import ParsedUnit
from bushido.modules.gym.domain import GymSpec
from bushido.modules.gym.orm import GymUnit


class GymMapper:
    def to_orm(self, parsed_unit: ParsedUnit[GymSpec]) -> tuple[GymUnit, list[Any]]:
        unit = GymUnit(name=parsed_unit.name, comment=parsed_unit.comment)
        return unit, []

    # TODO fix Any / None / []
    def from_orm(self, orms: tuple[GymUnit, list[Any]]) -> ParsedUnit[GymSpec]:
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
