from abc import ABC
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            relationship,
                            Session)


class Base(DeclarativeBase):
    __abstract__ = True
    key: Mapped[int] = mapped_column(primary_key=True)


class Category(Base):
    __tablename__ = 'category'
    name: Mapped[str] = mapped_column(unique=True)


class Emoji(Base):
    __tablename__ = 'emoji'
    emoji_base: Mapped[str] = mapped_column(unique=True)
    emoji_ext: Mapped[Optional[str]] = mapped_column()
    emoji_name: Mapped[str] = mapped_column(unique=True)
    unit_name: Mapped[str] = mapped_column(unique=True)
    category: Mapped[int] = mapped_column(ForeignKey(Category.key))


class Unit(Base):
    __tablename__ = 'unit'
    timestamp: Mapped[float] = mapped_column()
    emoji: Mapped[int] = mapped_column(ForeignKey(Emoji.key))


class Message(Base):
    __tablename__ = 'message'
    payload: Mapped[str] = mapped_column()
    comment: Mapped[Optional[str]] = mapped_column()
    unit: Mapped[int] = mapped_column(ForeignKey(Unit.key))


class Keiko(Base):
    __abstract__ = True
    unit: Mapped[int] = mapped_column(ForeignKey(Unit.key))


class BaseUploader(ABC):
    def __init__(self, engine):
        self.engine = engine
        self.unit = None

    def upload_unit(self, unix_timestamp, emoji_key, payload, comment, attrs):
        self._upload_unit(unix_timestamp, emoji_key)
        self._upload_message(payload, comment)
        self._upload_keiko(attrs)


    def _upload_unit(self, unix_timestamp, emoji_key):
        self.unit = Unit(unix_timestamp=unix_timestamp,
                         emoji=emoji_key)
        with Session(self.engine) as session:
            session.add(self.unit)
            session.commit()

    def _upload_message(self, payload, comment):
        message = Message(payload=payload,
                          comment=comment,
                          unit=self.unit.key)
        with Session(self.engine) as session:
            session.add(message)
            session.commit()

    def _upload_keiko(self, attrs):
        raise NotImplementedError


class BaseRetriever(ABC):
    def __init__(self, engine):
        self.engine = engine
