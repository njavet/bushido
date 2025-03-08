from abc import ABC
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column)


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
