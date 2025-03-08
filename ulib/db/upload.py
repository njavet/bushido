from abc import ABC
from typing import Optional
from sqlalchemy import ForeignKey, select
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            Session)


class Base(DeclarativeBase):
    __abstract__ = True
    key: Mapped[int] = mapped_column(primary_key=True)


class CategoryTable(Base):
    __tablename__ = 'category'
    name: Mapped[str] = mapped_column(unique=True)


class EmojiTable(Base):
    __tablename__ = 'emoji'
    base_emoji: Mapped[str] = mapped_column(unique=True)
    ext_emoji: Mapped[Optional[str]] = mapped_column()
    emoji_name: Mapped[str] = mapped_column(unique=True)
    unit_name: Mapped[str] = mapped_column(unique=True)
    fk_category: Mapped[int] = mapped_column(ForeignKey(CategoryTable.key))


class UnitTable(Base):
    __tablename__ = 'unit'
    timestamp: Mapped[float] = mapped_column()
    payload: Mapped[str] = mapped_column()
    comment: Mapped[Optional[str]] = mapped_column()
    fk_emoji: Mapped[int] = mapped_column(ForeignKey(EmojiTable.key))


class KeikoTable(Base):
    __abstract__ = True
    fk_unit: Mapped[int] = mapped_column(ForeignKey(UnitTable.key))


class BaseUploader(ABC):
    def __init__(self, engine):
        self.engine = engine
        self.unit = None

    def upload_unit(self, timestamp, payload, comment, emoji_key, attrs):
        self._create_unit(timestamp, payload, comment, emoji_key)
        self._upload_unit(attrs)

    def _create_unit(self, timestamp, payload, comment, emoji_key):
        self.unit = UnitTable(timestamp=timestamp,
                              payload=payload,
                              comment=comment,
                              fk_emoji=emoji_key)

    def _upload_unit(self, attrs):
        raise NotImplementedError


class BaseRetriever:
    def __init__(self, engine):
        self.engine = engine

    def get_emojis(self):
        stmt = (select(EmojiTable.base_emoji,
                       EmojiTable.ext_emoji,
                       CategoryTable.name,
                       EmojiTable.unit_name,
                       EmojiTable.key)
                .join(CategoryTable))
        with Session(self.engine) as session:
            emojis = session.execute(stmt).all()
        return emojis
