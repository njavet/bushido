from .unit import GymSpec, GymUnit
from .db_model import GymUnitTable


class GymMapper:
    @staticmethod
    def to_orm(parsed_unit: GymUnit) -> GymUnitTable:
        unit = GymUnitTable(
            name=parsed_unit.name,
            emoji=parsed_unit.emoji,
            log_time=parsed_unit.log_time,
            start_t=parsed_unit.data.start_t,
            end_t=parsed_unit.data.end_t,
            gym=parsed_unit.data.gym,
            training=parsed_unit.data.training,
            focus=parsed_unit.data.focus,
            comment=parsed_unit.comment,
        )
        return unit

    @staticmethod
    def from_orm(orm_unit: GymUnitTable) -> GymUnit:
        pu = GymUnit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            data=GymSpec(
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
