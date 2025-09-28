from typing import Any

from bushido.domain.gym import GymSpec
from bushido.domain.unit import ParsedUnit
from bushido.infra.db import GymUnit


class LiftingMapper:
    def to_orm(
        self, parsed_unit: ParsedUnit[GymSpec]
    ) -> tuple[GymUnit, list[Any]]:
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
                focus=unit.focus,
            ),
            comment=unit.comment,
        )
        return pu
