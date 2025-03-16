from abc import ABC
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, Session

# project import
from bushido.db.base_tables import Base, UnitTable, MDEmojiTable


class AbsCategory(ABC):
    def __init__(self, engine):
        self.engine = engine
        self.keiko = None
        self.emojis = None

    def receive_all(self, unit_name=None, start_t=None, end_t=None):
        if unit_name:
            stmt = (select(MDEmojiTable.base_emoji,
                           MDEmojiTable.ext_emoji,
                           UnitTable,
                           self.keiko)
                    .join(MDEmojiTable)
                    .join(UnitTable)
                    .where(MDEmojiTable.unit_name == unit_name))
        else:
            stmt = (select(MDEmojiTable.base_emoji,
                           MDEmojiTable.ext_emoji,
                           UnitTable,
                           self.keiko)
                    .join(MDEmojiTable)
                    .join(UnitTable))

        if start_t:
            start_timestamp = start_t.timestamp()
            stmt = stmt.where(start_timestamp <= UnitTable.timestamp)
        if end_t:
            end_timestamp = end_t.timestamp()
            stmt = stmt.where(UnitTable.timestamp <= end_timestamp)

        with Session(self.engine) as session:
            units = session.execute(stmt).all()
        return units


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
