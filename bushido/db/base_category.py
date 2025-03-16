from abc import ABC
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, Session

# project import
from bushido.db.base_tables import Base, UnitTable


class AbsCategory(ABC):
    def __init__(self, engine):
        self.engine = engine
        self.keiko = None

    def receive_all(self, unit_name=None, start_t=None, end_t=None):
        stmt = (select(UnitTable, self.keiko)
                .join(self.keiko))
        if unit_name:
            stmt = stmt.where()
        if start_t:
            start_timestamp = start_t.timestamp()
            stmt = stmt.where(start_timestamp <= UnitTable.timestamp)
        if end_t:
            end_timestamp = end_t.timestamp()
            stmt = stmt.where(UnitTable.timestamp <= end_timestamp)
        with Session(self.engine) as session:
            units = session.execute(stmt).all()


class AbsProcessor(ABC):
    def __init__(self, engine):
        self.engine = engine
        self.attrs = None

    def process_unit(self, timestamp, words, comment, emoji_key):
        unit = UnitTable(timestamp=timestamp,
                         payload=' '.join(words),
                         comment=comment,
                         fk_emoji=emoji_key)
        self.process_keiko(unit, words)

    def process_keiko(self, unit, words):
        raise NotImplementedError


class AbsKeikoTable(Base):
    __abstract__ = True
    fk_unit: Mapped[int] = mapped_column(ForeignKey(UnitTable.key))
