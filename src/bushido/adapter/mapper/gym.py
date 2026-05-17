from bushido.persistence.models import GymUnitTable
from bushido.units import Unit
from bushido.units.gym import GymData


class Mapper:
    @staticmethod
    def to_orm(unit: Unit[GymData]) -> GymUnitTable:
        orm_unit = GymUnitTable(
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
        return orm_unit

    @staticmethod
    def from_orm(orm_unit: GymUnitTable) -> Unit[GymData]:
        pu = Unit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            data=GymData(
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
