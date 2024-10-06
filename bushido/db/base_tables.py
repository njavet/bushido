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
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class Emoji(Base):
    __tablename__ = 'emoji'
    emoji_base: Mapped[str] = mapped_column(unique=True, nullable=False)
    emoji_ext: Mapped[str] = mapped_column(unique=True)
    emoji_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    unit_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    category: Mapped[str] = mapped_column(ForeignKey(Category.name),
                                          nullable=False)


class GymName(Base):
    __tablename__ = 'gym_name'
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class TrainingTopic(Base):
    __tablename__ = 'training_topic'
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class WorkProject(Base):
    __tablename__ = 'work_project'
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


class StudyTopic(Base):
    __tablename__ = 'study_topic'
    name: Mapped[str] = mapped_column(unique=True, nullable=False)


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
