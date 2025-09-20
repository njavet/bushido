from typing import Optional
from datetime import datetime, time, timedelta, timezone
from enum import StrEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import (String,
                        Integer,
                        DateTime,
                        ForeignKey,
                        Enum, UniqueConstraint, Float, Time, Interval, Text)
from sqlalchemy import ForeignKey


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class UnitModel(Base):
    __tablename__ = 'unit'
    ts_utc: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), index=True
    )
    payload: Mapped[str] = mapped_column()
    comment: Mapped[str | None] = mapped_column()
    fk_emoji: Mapped[int] = mapped_column(ForeignKey(MDEmojiModel.id))


class TrainingType(StrEnum):
    weights = 'weights'
    cardio = 'cardio'
    martial_arts = 'martial_arts'
    stretching = 'stretching'


class Location(Base):
    __tablename__ = 'location'
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)


class Training(Base):
    __tablename__ = 'training'
    id: Mapped[int] = mapped_column(primary_key=True)
    ts_start: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)
    ts_end: Mapped[Optional[datetime]]
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey('location.id'))
    note: Mapped[Optional[str]] = mapped_column(Text)

    location: Mapped[Optional[Location]] = relationship()
    entries: Mapped[list[Entry]] = relationship(back_populates='workout', cascade='all, delete-orphan')


class Entry(Base):
    """
    Aggregate root for a single logged item (weights set group, a run, a sparring block, a bodystat, a study block).
    """
    __tablename__ = 'entry'
    id: Mapped[int] = mapped_column(primary_key=True)
    workout_id: Mapped[int] = mapped_column(ForeignKey('workout.id', ondelete='CASCADE'), index=True)
    kind: Mapped[ActivityType] = mapped_column(Enum(ActivityType), index=True)
    ts: Mapped[datetime] = mapped_column(default=datetime.utcnow, index=True)
    label: Mapped[Optional[str]] = mapped_column(String(120))  # free label or emoji alias
    note: Mapped[Optional[str]] = mapped_column(Text)

    workout: Mapped[Workout] = relationship(back_populates='entries')
    weights: Mapped[Optional[WeightsEntry]] = relationship(back_populates='entry', uselist=False, cascade='all, delete-orphan')
    cardio:  Mapped[Optional[CardioEntry]]  = relationship(back_populates='entry', uselist=False, cascade='all, delete-orphan')
    martial: Mapped[Optional[MartialEntry]] = relationship(back_populates='entry', uselist=False, cascade='all, delete-orphan')
    stat:    Mapped[Optional[BodyStatEntry]] = relationship(back_populates='entry', uselist=False, cascade='all, delete-orphan')
    study:   Mapped[Optional[StudyEntry]] = relationship(back_populates='entry', uselist=False, cascade='all, delete-orphan')

# ------- Weights
class WeightsEntry(Base):
    __tablename__ = 'weights_entry'
    id: Mapped[int] = mapped_column(primary_key=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey('entry.id', ondelete='CASCADE'), unique=True)
    exercise: Mapped[str] = mapped_column(String(120), index=True)  # e.g. 'squat', 'bench'
    tempo: Mapped[Optional[str]] = mapped_column(String(20))
    rir: Mapped[Optional[int]]
    entry: Mapped[Entry] = relationship(back_populates='weights')
    sets: Mapped[list[WeightsSet]] = relationship(back_populates='weights', cascade='all, delete-orphan')

class WeightsSet(Base):
    __tablename__ = 'weights_set'
    id: Mapped[int] = mapped_column(primary_key=True)
    weights_id: Mapped[int] = mapped_column(ForeignKey('weights_entry.id', ondelete='CASCADE'), index=True)
    kg: Mapped[float] = mapped_column(Float)
    reps: Mapped[int] = mapped_column(Integer)
    rest: Mapped[Optional[int]] = mapped_column(Integer)  # seconds
    __table_args__ = (UniqueConstraint('weights_id','id', name='uq_weightsset_identity'),)
    weights: Mapped[WeightsEntry] = relationship(back_populates='sets')

# ------- Cardio
class CardioType(StrEnum):
    run = 'run'
    bike = 'bike'
    row = 'row'
    swim = 'swim'
    other = 'other'

class CardioEntry(Base):
    __tablename__ = 'cardio_entry'
    id: Mapped[int] = mapped_column(primary_key=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey('entry.id', ondelete='CASCADE'), unique=True)
    mode: Mapped[CardioType] = mapped_column(Enum(CardioType), index=True)
    start_clock: Mapped[Optional[time]]
    duration: Mapped[Optional[timedelta]]
    distance_km: Mapped[Optional[float]]
    avg_hr: Mapped[Optional[int]]
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey('location.id'))
    entry: Mapped[Entry] = relationship(back_populates='cardio')
    location: Mapped[Optional[Location]] = relationship()

# ------- Martial
class MartialStyle(StrEnum):
    bjj = 'bjj'
    wrestling = 'wrestling'
    kyokushin = 'kyokushin'
    judo = 'judo'
    boxing = 'boxing'
    other = 'other'

class MartialEntry(Base):
    __tablename__ = 'martial_entry'
    id: Mapped[int] = mapped_column(primary_key=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey('entry.id', ondelete='CASCADE'), unique=True)
    style: Mapped[MartialStyle] = mapped_column(Enum(MartialStyle), index=True)
    minutes: Mapped[int]
    rpe: Mapped[Optional[int]]
    rounds: Mapped[Optional[int]]
    entry: Mapped[Entry] = relationship(back_populates='martial')

# ------- Body stats
class BodyStatEntry(Base):
    __tablename__ = 'bodystat_entry'
    id: Mapped[int] = mapped_column(primary_key=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey('entry.id', ondelete='CASCADE'), unique=True)
    weight_kg: Mapped[Optional[float]]
    bodyfat_pct: Mapped[Optional[float]]
    waist_cm: Mapped[Optional[float]]
    sleep_h: Mapped[Optional[float]]
    soreness: Mapped[Optional[int]]
    entry: Mapped[Entry] = relationship(back_populates='stat')

# ------- Study
class StudyEntry(Base):
    __tablename__ = 'study_entry'
    id: Mapped[int] = mapped_column(primary_key=True)
    entry_id: Mapped[int] = mapped_column(ForeignKey('entry.id', ondelete='CASCADE'), unique=True)
    topic: Mapped[str] = mapped_column(String(160), index=True)
    minutes: Mapped[int]
    pomodoros: Mapped[Optional[int]]
    entry: Mapped[Entry] = relationship(back_populates='study')