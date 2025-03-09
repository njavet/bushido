from abc import ABC
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# project import
from ulib.db import Base, UnitTable


class AbsCategory(ABC):
    def __init__(self, name, engine):
        self.name = name
        self.engine = engine
        self.keiko = None


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
