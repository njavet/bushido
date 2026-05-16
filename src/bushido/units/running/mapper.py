from .db_model import CardioUnitTable
from .unit import CardioSpec, CardioUnit


class CardioMapper:
    @staticmethod
    def to_orm(parsed_unit: CardioUnit) -> CardioUnitTable:
        unit = CardioUnitTable(
            name=parsed_unit.name,
            emoji=parsed_unit.emoji,
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
    def from_orm(orm_unit: CardioUnitTable) -> CardioUnit:
        pu = CardioUnit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
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
