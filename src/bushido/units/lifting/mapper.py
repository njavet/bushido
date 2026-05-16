from ..base import Unit
from .db_model import LiftingUnitTable
from .unit import LiftingData


class LiftingMapper:
    @staticmethod
    def to_orm(unit: Unit[LiftingData]) -> LiftingUnitTable:
        unit = LiftingUnitTable(
            name=unit.name,
            emoji=unit.emoji,
            log_time=unit.log_time,
            start_t=unit.data.start_t,
            end_t=unit.data.end_t,
            gym=unit.data.gym,
            training=unit.data.training,
            focus=unit.data.focus,
            comment=unit.comment,
        )
        return unit

    @staticmethod
    def from_orm(orm_unit: LiftingUnitTable) -> Unit[LiftingData]:
        pu = Unit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            data=LiftingData(
                start_t=orm_unit.start_t,
                end_t=orm_unit.end_t,
                gym=orm_unit.gym,
                training=orm_unit.training,
                focus=orm_unit.focus,
            ),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
