from typing import Any

from bushido.core.dtypes import ParsedUnit
from bushido.modules.mapper import UnitMapper

from .domain import CardioSpec
from .orm import CardioUnit


class CardioMapper(UnitMapper[CardioSpec, CardioUnit, Any]):
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[CardioSpec]) -> tuple[CardioUnit, list[Any]]:
        unit = CardioUnit(
            name=parsed_unit.name,
            log_time=parsed_unit.log_time,
            start_t=parsed_unit.data.start_t,
            seconds=parsed_unit.data.seconds,
            location=parsed_unit.data.location,
            distance=parsed_unit.data.distance,
            avg_hr=parsed_unit.data.avg_hr,
            max_hr=parsed_unit.data.max_hr,
            calories=parsed_unit.data.calories,
            comment=parsed_unit.comment,
        )
        return unit, []

    # TODO fix Any / None / []
    @staticmethod
    def from_orm(orms: tuple[CardioUnit, list[Any]]) -> ParsedUnit[CardioSpec]:
        unit, _ = orms
        pu = ParsedUnit(
            name=unit.name,
            data=CardioSpec(
                start_t=unit.start_t,
                seconds=unit.seconds,
                location=unit.location,
                distance=unit.distance,
                avg_hr=unit.avg_hr,
                max_hr=unit.max_hr,
                calories=unit.calories,
            ),
            log_time=unit.log_time,
            comment=unit.comment,
        )
        return pu
