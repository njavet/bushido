from bushido.persistence.models import LiftingSet, LiftingUnitTable
from bushido.units import Unit
from bushido.units.lifting import LiftingData, SetData


class Mapper:
    @staticmethod
    def to_orm(unit: Unit[LiftingData]) -> LiftingUnitTable:
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
    def from_orm(orm_unit: LiftingUnitTable) -> Unit[LiftingData]:
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


import datetime
from typing import Generic, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.interfaces import ORMOption

from .models.base import UnitTable

T_ORM = TypeVar("T_ORM", bound=UnitTable)


class UnitRepo(Generic[T_ORM]):
    def __init__(
        self,
        session: Session,
        load_options: Sequence[ORMOption] = (),
    ) -> None:
        self.session = session
        self.load_options = load_options

    def add_unit(self, unit: T_ORM) -> None:
        self.session.add(unit)
        self.session.commit()

    def fetch_units(
        self,
        unit_name: str | None = None,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> Sequence[T_ORM]:
        stmt = select(UnitTable).options(*self.load_options)
        if unit_name is not None:
            stmt = stmt.where(UnitTable.name == unit_name)
        if start_t is not None:
            stmt = stmt.where(start_t <= UnitTable.log_time)
        if end_t is not None:
            stmt = stmt.where(UnitTable.log_time <= end_t)
        stmt = stmt.order_by(UnitTable.log_time.desc())
        return list(self.session.scalars(stmt))
