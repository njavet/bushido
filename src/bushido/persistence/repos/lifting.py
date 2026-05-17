import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from bushido.units import Unit
from bushido.units.lifting import LiftingData, SetData

from ..models import LiftingSet, LiftingUnitTable


class LiftingUnitRepo:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_unit(self, unit: Unit[LiftingData]) -> None:
        self.session.add(unit)
        self.session.commit()

    def fetch_units(
        self,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit[LiftingData]]:
        stmt = select(LiftingUnitTable).options(selectinload(LiftingUnitTable.subunits))
        if start_t is not None:
            stmt = stmt.where(start_t <= LiftingUnitTable.log_time)
        if end_t is not None:
            stmt = stmt.where(LiftingUnitTable.log_time <= end_t)
        stmt = stmt.order_by(LiftingUnitTable.log_time.desc())
        return [self._from_orm(unit) for unit in self.session.scalars(stmt)]

    @staticmethod
    def _to_orm(unit: Unit[LiftingData]) -> LiftingUnitTable:
        orm_unit = LiftingUnitTable(
            name=unit.name,
            emoji=unit.emoji,
            comment=unit.comment,
            log_time=unit.log_time,
        )
        orm_unit.subunits = [
            LiftingSet(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            for s in unit.data.sets
        ]
        return orm_unit

    @staticmethod
    def _from_orm(orm_unit: LiftingUnitTable) -> Unit[LiftingData]:
        lst = []
        for s in orm_unit.subunits:
            sp = SetData(set_nr=s.set_nr, weight=s.weight, reps=s.reps, rest=s.rest)
            lst.append(sp)
        pu = Unit(
            name=orm_unit.name,
            emoji=orm_unit.emoji,
            data=LiftingData(sets=lst, program=None, variant=None),
            log_time=orm_unit.log_time,
            comment=orm_unit.comment,
        )
        return pu
