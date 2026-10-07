import datetime
from abc import ABC, abstractmethod
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.interfaces import ORMOption

from citadel.domain.unit import BaseUnit, UnitType

from ..models import UnitTable


class BaseUnitRepo[UnitT: BaseUnit, OrmT: UnitTable](ABC):
    orm_cls: type[OrmT]
    unit_type: UnitType
    load_options: Sequence[ORMOption] = ()

    def __init__(self, session: Session) -> None:
        self.session = session

    @abstractmethod
    def add_unit(self, unit: UnitT, spartan_id: int) -> None: ...

    def fetch_units(
        self,
        spartan_id: int,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[UnitT]:
        stmt = (
            select(self.orm_cls)
            .where(self.orm_cls.spartan_id == spartan_id)
            .options(*self.load_options)
        )
        if start_t is not None:
            stmt = stmt.where(start_t <= self.orm_cls.log_time)
        if end_t is not None:
            stmt = stmt.where(self.orm_cls.log_time <= end_t)
        stmt = stmt.order_by(self.orm_cls.log_time.desc())
        return [self._from_orm(unit) for unit in self.session.scalars(stmt)]

    @abstractmethod
    def _from_orm(self, orm_unit: OrmT) -> UnitT: ...
