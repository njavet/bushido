from bushido.units.base import Unit

from .db_model import RunningUnitTable
from .unit import RunningData


class RunningMapper:
    @staticmethod
    def to_orm(unit: Unit[RunningData]) -> RunningUnitTable:
        orm_unit = RunningUnitTable(
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
    def from_orm(orm_unit: RunningUnitTable) -> Unit[RunningData]:
        pu = Unit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            data=RunningData(
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
