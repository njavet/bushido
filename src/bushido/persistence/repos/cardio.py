import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from bushido.units import Unit
from bushido.units.cardio import CardioData

from ..models import CardioUnitTable


class CardioUnitRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_unit(self, unit: Unit[CardioData]) -> None:
        self.session.add(self._to_orm(unit))
        self.session.commit()

    def fetch_units(
        self,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit[CardioData]]:
        stmt = select(CardioUnitTable)
        if start_t is not None:
            stmt = stmt.where(start_t <= CardioUnitTable.log_time)
        if end_t is not None:
            stmt = stmt.where(CardioUnitTable.log_time <= end_t)
        stmt = stmt.order_by(CardioUnitTable.log_time.desc())
        return [self._from_orm(unit) for unit in self.session.scalars(stmt)]

    @staticmethod
    def _to_orm(unit: Unit[CardioData]) -> CardioUnitTable:
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
    def _from_orm(orm_unit: CardioUnitTable) -> Unit[CardioData]:
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
