from ..dtypes import ParsedUnit
from .orm import CardioUnitTable
from .parser import CardioSpec


class CardioMapper:
    @staticmethod
    def to_orm(parsed_unit: ParsedUnit[CardioSpec]) -> CardioUnitTable:
        unit = CardioUnitTable(
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
        return unit

    @staticmethod
    def from_orm(orm_unit: CardioUnitTable) -> ParsedUnit[CardioSpec]:
        pu = ParsedUnit(
            name=orm_unit.name,
            data=CardioSpec(
                start_t=orm_unit.start_t,
                seconds=orm_unit.seconds,
                location=orm_unit.location,
                distance=orm_unit.distance,
                avg_hr=orm_unit.avg_hr,
                max_hr=orm_unit.max_hr,
                calories=orm_unit.calories,
            ),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
