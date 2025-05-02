import datetime
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column)


class Base(DeclarativeBase):
    __abstract__ = True
    key: Mapped[int] = mapped_column(primary_key=True)


class MDEmojiModel(Base):
    __tablename__ = 'md_emoji'
    unit_name: Mapped[str] = mapped_column(unique=True)
    emoji_name: Mapped[str] = mapped_column(unique=True)
    emoticon: Mapped[str] = mapped_column(unique=True)
    emoji: Mapped[str] = mapped_column(unique=True)


class UnitModel(Base):
    __tablename__ = 'unit'
    timestamp: Mapped[int] = mapped_column()
    payload: Mapped[str] = mapped_column()
    comment: Mapped[Optional[str]] = mapped_column()
    fk_emoji: Mapped[int] = mapped_column(ForeignKey(MDEmojiModel.key))


class DayModel(Base):
    __tablename__ = 'day'

    date_: Mapped[datetime.date] = mapped_column(unique=True)
    # TODO default values 0400 start, 0359 end
    start_t: Mapped[datetime.time] = mapped_column()
    end_t: Mapped[datetime.time] = mapped_column()

    body_weight: Mapped[float] = mapped_column()


