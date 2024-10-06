from sqlalchemy import ForeignKey
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            relationship)


class Base(DeclarativeBase):
    __abstract__ = True
    id_: Mapped[int] = mapped_column(primary_key=True)


class Category(Base):
    __tablename__ = 'category'
    name: Mapped[str] = mapped_column(unique=True)


class Emoji(Base):
    __tablename__ = 'emoji'
    emoji: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)
    category: Mapped[str] = mapped_column(ForeignKey(Category.name),
                                          nullable=False)


class Unit(Base):
    __tablename__ = 'unit'
    unix_timestamp: Mapped[float] = mapped_column(nullable=False)
    emoji: Mapped[str] = mapped_column(ForeignKey(Emoji.name))


class Message(Base):
    __tablename__ = 'message'
    payload: Mapped[str] = mapped_column()
    comment: Mapped[str] = mapped_column()
    unit: Mapped[int] = mapped_column(ForeignKey(Unit.id_),
                                      nullable=False)


class Keiko(Base):
    __abstract__ = True
    unit: Mapped[int] = mapped_column(ForeignKey(Unit.id_),
                                      nullable=False)
