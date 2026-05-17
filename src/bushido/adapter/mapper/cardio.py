from bushido.db.models import CardioUnitTable
from bushido.units import Unit
from bushido.units.cardio import CardioData


class Mapper:
    @staticmethod
    def to_orm(unit: Unit[CardioData]) -> CardioUnitTable:
        orm_unit = CardioUnitTable(
            name=unit.name,
            emoji=unit.emoji,
            log_time=unit.log_time,
            start_t=unit.data.start_t,
            seconds=unit.data.seconds,
            location=unit.data.location,
            distance=unit.data.distance,
            avg_hr=unit.data.avg_hr,
            max_hr=unit.data.max_hr,
            calories=unit.data.calories,
            comment=unit.comment,
        )
        return orm_unit

    @staticmethod
    def from_orm(orm_unit: CardioUnitTable) -> Unit[CardioData]:
        pu = Unit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            data=CardioData(
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
