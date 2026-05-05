from .domain import GymSpec, GymUnit
from .orm import GymUnitTable


class GymMapper:
    @staticmethod
    def to_orm(parsed_unit: GymUnit) -> GymUnitTable:
        unit = GymUnitTable(
            name=parsed_unit.name,
            log_time=parsed_unit.log_time,
            start_t=parsed_unit.data.start_t,
            end_t=parsed_unit.data.end_t,
            location=parsed_unit.data.location,
            training=parsed_unit.data.training,
            focus=parsed_unit.data.focus,
            comment=parsed_unit.comment,
        )
        return unit

    @staticmethod
    def from_orm(orm_unit: GymUnitTable) -> GymUnit:
        pu = GymUnit(
            name=orm_unit.name,
            data=GymSpec(
                start_t=orm_unit.start_t,
                end_t=orm_unit.end_t,
                location=orm_unit.location,
                training=orm_unit.training,
                focus=orm_unit.focus,
            ),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
