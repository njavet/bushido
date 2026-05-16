from bushido.units.base import Unit

from .db_model import MartialArtsUnitTable
from .unit import MartialArtsData


class MartialArtsMapper:
    @staticmethod
    def to_orm(unit: Unit[MartialArtsData]) -> MartialArtsUnitTable:
        orm_unit = MartialArtsUnitTable(
            name=unit.name,
            emoji=unit.emoji,
            log_time=unit.log_time,
            start_t=unit.data.start_t,
            end_t=unit.data.end_t,
            gym=unit.data.gym,
            sensei=unit.data.sensei,
            training=unit.data.training,
            focus=unit.data.focus,
            comment=unit.comment,
        )
        return orm_unit

    @staticmethod
    def from_orm(orm_unit: MartialArtsUnitTable) -> Unit[MartialArtsData]:
        pu = Unit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            data=MartialArtsData(
                start_t=orm_unit.start_t,
                end_t=orm_unit.end_t,
                gym=orm_unit.gym,
                sensei=orm_unit.sensei,
                training=orm_unit.training,
                focus=orm_unit.focus,
            ),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
