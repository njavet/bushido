from typing import Generic, Protocol, TypeVar

from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute, Session, selectinload

from bushido.infra.db.model.base import Unit


class Subunit(Protocol):
    id: int
    fk_unit: int


U = TypeVar('U', bound=Unit)
S = TypeVar('S', bound=Subunit)


class UnitRepo(Generic[U, S]):
    def __init__(
        self,
        session: Session,
        unit_cls: type[U],
        subrels: InstrumentedAttribute[list[S]] | None = None,
    ) -> None:
        self.session = session
        self.unit_cls = unit_cls
        self.subrels = subrels

    # TODO handle exceptions
    def add_unit(self, unit: U, subs: list[S] | None = None) -> bool:
        if self.subrels is not None:
            getattr(unit, self.subrels.key).extend(subs)
        self.session.add(unit)
        self.session.commit()
        return True

    def fetch_units(self, unit_name: str | None = None) -> list[U]:
        stmt = select(self.unit_cls)
        if unit_name is not None:
            stmt = stmt.where(getattr(self.unit_cls, 'name') == unit_name)
        if self.subrels is not None:
            stmt = stmt.options(selectinload(self.subrels))
        return list(self.session.scalars(stmt))
