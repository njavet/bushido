from abc import ABC
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import Mapped, mapped_column, Session

# project import
from bushido.data.base import Base, UnitTable, MDEmojiTable


class AbsCategory(ABC):
    def __init__(self, engine):
        self.engine = engine
        self.keiko = None

    def receive_all(self, unit_name=None, start_t=None, end_t=None):
        stmt = (select(MDEmojiTable.base_emoji,
                       MDEmojiTable.ext_emoji,
                       UnitTable.timestamp,
                       UnitTable.payload,
                       UnitTable.comment,
                       self.keiko)
                .join(UnitTable, MDEmojiTable.key == UnitTable.fk_emoji)
                .join(self.keiko, UnitTable.key == self.keiko.fk_unit))
        if unit_name:
            stmt = stmt.where(MDEmojiTable.unit_name == unit_name)
        if start_t:
            start_timestamp = start_t.timestamp()
            stmt = stmt.where(start_timestamp <= UnitTable.timestamp)
        if end_t:
            end_timestamp = end_t.timestamp()
            stmt = stmt.where(UnitTable.timestamp <= end_timestamp)

        with Session(self.engine) as session:
            units = session.execute(stmt).all()
        return units


class AbsKeikoTable(Base):
    __abstract__ = True
    fk_unit: Mapped[int] = mapped_column(ForeignKey(UnitTable.key))
