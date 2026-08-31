import datetime
from abc import ABC, abstractmethod
from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.interfaces import ORMOption

from bushidolib.constants import UnitCategory
from bushidolib.unit import BaseUnit, UnitSetting

from ..models import UnitCategoryTable, UnitConfigTable, UnitTable


class BaseUnitRepo[T_DOMAIN: BaseUnit, T_ORM: UnitTable](ABC):
    orm_cls: type[T_ORM]
    load_options: Sequence[ORMOption] = ()

    def __init__(self, session: Session) -> None:
        self.session = session

    def get_unit_setting_id(self, unit_name: str) -> int:
        stmt = select(UnitConfigTable.id).where(UnitConfigTable.name == unit_name)
        return self.session.scalars(stmt).one()

    def get_unit_setting_name(self, setting_id: int) -> str:
        stmt = select(UnitConfigTable.name).where(UnitConfigTable.id == setting_id)
        return self.session.scalars(stmt).one()

    def add_unit(self, unit: T_DOMAIN) -> None:
        self.session.add(self._to_orm(unit))
        self.session.commit()

    def fetch_units(
        self,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[T_DOMAIN]:
        stmt = select(self.orm_cls).options(*self.load_options)
        if start_t is not None:
            stmt = stmt.where(start_t <= self.orm_cls.log_time)
        if end_t is not None:
            stmt = stmt.where(self.orm_cls.log_time <= end_t)
        stmt = stmt.order_by(self.orm_cls.log_time.desc())
        return [self._from_orm(unit) for unit in self.session.scalars(stmt)]

    @abstractmethod
    def _to_orm(self, unit: T_DOMAIN) -> T_ORM: ...

    @abstractmethod
    def _from_orm(self, orm_unit: T_ORM) -> T_DOMAIN: ...


def load_unit_settings(session: Session) -> list[UnitSetting]:
    stmt = select(
        UnitConfigTable.name,
        UnitCategoryTable.name.label("category"),
    ).join(
        UnitCategoryTable,
        UnitConfigTable.category_id == UnitCategoryTable.id,
    )

    result = session.execute(stmt).all()
    return [UnitSetting(name=r.name, category=UnitCategory(r.category)) for r in result]
