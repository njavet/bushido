from .db_model import LiftingUnitTable
from .unit import GymUnit


class GymMapper:
    @staticmethod
    def to_orm(unit: GymUnit) -> LiftingUnitTable:
        unit = LiftingUnitTable(
            name=unit.name,
            emoji=unit.emoji,
            log_time=unit.log_time,
            start_t=unit.start_t,
            end_t=unit.end_t,
            gym=unit.gym,
            training=unit.training,
            focus=unit.focus,
            comment=unit.comment,
        )
        return unit

    @staticmethod
    def from_orm(orm_unit: LiftingUnitTable) -> GymUnit:
        pu = GymUnit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            start_t=orm_unit.start_t,
            end_t=orm_unit.end_t,
            gym=orm_unit.gym,
            training=orm_unit.training,
            focus=orm_unit.focus,
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
