from abc import ABC
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column

# project import
from bushido.db.base_tables import Base, UnitTable


class AbsCategory(ABC):
    def __init__(self, engine):
        self.engine = engine
        self.keiko = None

    def receive_all(self, unit_name=None, start_t=None, end_t=None):
        stmt = (select(UnitTable)
                .join(self.keiko))


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
