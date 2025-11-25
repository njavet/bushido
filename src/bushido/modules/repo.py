import datetime
from typing import Generic

from sqlalchemy import select
from sqlalchemy.orm import InstrumentedAttribute, Session, selectinload

from bushido.modules.dtypes import TS, TU

# TODO add stricter typing
"""
from typing import Protocol

class HasSubunits(Generic[S], Protocol):
    subunits: Mapped[list[S]]

class RepoWithSubs(Generic[U, S]):
    def __init__(self, 
    s: Session, unit_cls: type[U], rel: InstrumentedAttribute[list[S]]): ...
    # add_unit and fetch_units eager-load rel

class FlatRepo(Generic[U]):
    def __init__(self, s: Session, unit_cls: type[U]): ...
    # add_unit (no subs) and fetch_units (no eager-load)
"""


class UnitRepo(Generic[TU, TS]):
    def __init__(
        self,
        session: Session,
        unit_cls: type[TU]class UnitSuggester(Suggester):
    def __init__(self, emojis: dict[str, str]) -> None:
        super().__init__()
        self.emojis = emojis
        self.un2emoji = self.construct_dict()

    def construct_dict(self) -> dict[str, str]:
        dix: dict[str, str] = {}
        for e, n in self.emojis.items():
            dix[n] = e
        return dix

    async def get_suggestion(self, value: str) -> str | None:
        es = [
            umoji for uname, umoji in self.un2emoji.items() if uname.startswith(value)
        ]
        if len(es) == 1:
            # TODO different emoji length
            return es[0] + "  "
        return None


class TextInput(Input):
    def __init__(self, placeholder: str, suggester: UnitSuggester) -> None:
        super().__init__(placeholder=placeholder, suggester=suggester, id="text_input")

    def on_suggestion_ready(self, event: SuggestionReady) -> None:
        self.action_delete_left_all()
        self.insert_text_at_cursor(event.suggestion)

    def on_key(self, event: Key) -> None:
        # workaround for accepting autocompletion
        if event.key == "space":
            self.action_cursor_right()
,
        subrels: InstrumentedAttribute[list[TS]] | None = None,
    ) -> None:
        self.session = session
        self.unit_cls = unit_cls
        self.subrels = subrels

    # TODO handle exceptions
    def add_unit(self, unit: TU, subs: list[TS] | None = None) -> bool:
        if self.subrels is not None:
            getattr(unit, self.subrels.key).extend(subs)
        self.session.add(unit)
        self.session.commit()
        return True

    def fetch_units(
        self,
        unit_name: str | None = None,
        start_t: datetime.datetime | None = None,
        end_t: datetime.datetime | None = None,
    ) -> list[TU]:
        stmt = select(self.unit_cls)
        if unit_name is not None:
            stmt = stmt.where(self.unit_cls.name == unit_name)
        if self.subrels is not None:
            stmt = stmt.options(selectinload(self.subrels))
        stmt = stmt.order_by(self.unit_cls.log_time, desc=True)
        return list(self.session.scalars(stmt))
