from typing import Any

from bushido.core.dtypes import ParsedUnit, UnitMapper

from .domain import GymSpec
from .orm import GymUnit


class GymMapper(UnitMapper[GymSpec, GymUnit, Any]):
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[GymSpec]) -> tuple[GymUnit, list[Any]]:
        unit = GymUnit(
            name=parsed_unit.name,
            log_time=parsed_unit.log_time,
            start_t=parsed_unit.data.start_t,
            end_t=parsed_unit.data.end_t,
            location=parsed_unit.data.location,
            training=parsed_unit.data.training,
            focus=parsed_unit.data.focus,
            comment=parsed_unit.comment,
        )
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
            log_time=unit.log_time,
            comment=unit.comment,
        )
        return pu
