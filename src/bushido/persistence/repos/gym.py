import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from bushido.units import Unit
from bushido.units.gym import GymData

from ..models import GymUnitTable


class GymUnitRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_unit(self, unit: Unit[GymData]) -> None:
        self.session.add(self._to_orm(unit))
        self.session.commit()

    def fetch_units(
        self,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit[GymData]]:
        stmt = select(GymUnitTable)
        if start_t is not None:
            stmt = stmt.where(start_t <= GymUnitTable.log_time)
        if end_t is not None:
            stmt = stmt.where(GymUnitTable.log_time <= end_t)
        stmt = stmt.order_by(GymUnitTable.log_time.desc())
        return [self._from_orm(unit) for unit in self.session.scalars(stmt)]

    @staticmethod
    def _to_orm(unit: Unit[GymData]) -> GymUnitTable:
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
    def _from_orm(orm_unit: GymUnitTable) -> Unit[GymData]:
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
