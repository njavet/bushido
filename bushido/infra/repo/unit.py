from typing import Generic, Protocol, TypeVar

from sqlalchemy.orm import InstrumentedAttribute, Session

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
    def add_unit(self, unit: U, subs: list[S] = []) -> bool:
        if self.subrels is not None:
            getattr(unit, self.subrels.key).extend(subs)
        self.session.add(unit)
        self.session.commit()
        return True
