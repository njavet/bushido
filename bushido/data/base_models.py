from sqlalchemy import ForeignKey
from typing import Optional
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column)


class Base(DeclarativeBase):
    __abstract__ = True
    key: Mapped[int] = mapped_column(primary_key=True)


class MDCategoryTable(Base):
    __tablename__ = 'md_category'
    name: Mapped[str] = mapped_column(unique=True)


class MDEmojiTable(Base):
    __tablename__ = 'md_emoji'
    unit_name: Mapped[str] = mapped_column(unique=True)
    emoji_name: Mapped[str] = mapped_column(unique=True)
    emoticon: Mapped[str] = mapped_column(unique=True)
    emoji: Mapped[str] = mapped_column(unique=True)
    fk_category: Mapped[int] = mapped_column(ForeignKey(MDCategoryTable.key))


class UnitTable(Base):
    __tablename__ = 'unit'
    timestamp: Mapped[int] = mapped_column()
    payload: Mapped[str] = mapped_column()
    comment: Mapped[Optional[str]] = mapped_column()
    fk_emoji: Mapped[int] = mapped_column(ForeignKey(MDEmojiTable.key))


class AbsKeikoTable(Base):
    __abstract__ = True
    fk_unit: Mapped[int] = mapped_column(ForeignKey(UnitTable.key))


class WimhofModel(AbsKeikoTable):
    __tablename__ = 'wimhof'

    round_nr: Mapped[int] = mapped_column()
    breaths: Mapped[int] = mapped_column()
    retention: Mapped[int] = mapped_column()


class LiftingModel(AbsKeikoTable):
    __tablename__ = 'lifting'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)


class ScaleModel(AbsKeikoTable):
    __tablename__ = 'scale'

    weight: Mapped[float] = mapped_column()
    belly: Mapped[Optional[float]] = mapped_column()
