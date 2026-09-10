import datetime
from abc import ABC, abstractmethod
from collections.abc import Sequence

from bushidolib.category.base.unit import Unit
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.interfaces import ORMOption

from ..models import UnitTable


class UnitRepo[UnitDataT, OrmT: UnitTable](ABC):
    orm_cls: type[OrmT]
    data_cls: type[UnitDataT]
    load_options: Sequence[ORMOption] = ()

    def __init__(self, session: Session) -> None:
        self.session = session

    def add_unit(self, unit: Unit) -> None:
        self.session.add(self._to_orm(unit))
        self.session.commit()

    def fetch_units(
        self,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[Unit]:
        stmt = select(self.orm_cls).options(*self.load_options)
        if start_t is not None:
            stmt = stmt.where(start_t <= self.orm_cls.log_time)
        if end_t is not None:
            stmt = stmt.where(self.orm_cls.log_time <= end_t)
        stmt = stmt.order_by(self.orm_cls.log_time.desc())
        return [self._from_orm(unit) for unit in self.session.scalars(stmt)]

    @abstractmethod
    def _to_orm(self, unit: Unit) -> OrmT: ...

    def _unit_data_to_orm(self, data: UnitDataT) -> dict:
        return {k: v for k, v in data.model_dump().items() if v is not None}

    @abstractmethod
    def _from_orm(self, orm_unit: OrmT) -> Unit: ...
