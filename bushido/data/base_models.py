import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column)

# project imports
from bushido.conf import DAY_START_HOUR


class Base(DeclarativeBase):
    __abstract__ = True
    key: Mapped[int] = mapped_column(primary_key=True)


class MDCategoryModel(Base):
    __tablename__ = 'md_category'
    name: Mapped[str] = mapped_column(unique=True)


class MDEmojiModel(Base):
    __tablename__ = 'md_emoji'
    unit_name: Mapped[str] = mapped_column(unique=True)
    emoji_name: Mapped[str] = mapped_column(unique=True)
    emoticon: Mapped[str] = mapped_column(unique=True)
    emoji: Mapped[str] = mapped_column(unique=True)
    fk_category: Mapped[int] = mapped_column(ForeignKey(MDCategoryModel.key))


class UnitModel(Base):
    __tablename__ = 'unit'
    timestamp: Mapped[int] = mapped_column()
    payload: Mapped[str] = mapped_column()
    comment: Mapped[Optional[str]] = mapped_column()
    fk_emoji: Mapped[int] = mapped_column(ForeignKey(MDEmojiModel.key))


class DayModel(Base):
    __tablename__ = 'day'

    date: Mapped[datetime.date] = mapped_column(unique=True)
    start_time: Mapped[datetime.time] = mapped_column()
    end_time: Mapped[datetime.time] = mapped_column()
    status: Mapped[Optional[int]] = mapped_column()
    mood: Mapped[Optional[str]] = mapped_column()
    comment: Mapped[Optional[str]] = mapped_column()


class AbsKeikoModel(Base):
    __abstract__ = True
    fk_unit: Mapped[int] = mapped_column(ForeignKey(UnitModel.key))
