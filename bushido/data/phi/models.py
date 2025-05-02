from typing import Optional
from datetime import time
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# project imports
from bushido.data.base_models import Base


class TrainingModel(Base):
    __tablename__ = 'training'

    training_type: Mapped[str] = mapped_column()
    start_ts: Mapped[int] = mapped_column()
    end_ts: Mapped[int] = mapped_column()
    gym: Mapped[str] = mapped_column()


class CardioModel(Base):
    __tablename__ = 'cardio'

    seconds: Mapped[float] = mapped_column()
    distance: Mapped[Optional[float]] = mapped_column()
    avg_hr: Mapped[Optional[int]] = mapped_column()
    max_hr: Mapped[Optional[int]] = mapped_column()
    cal: Mapped[Optional[int]] = mapped_column()

    fk_training: Mapped[int] = mapped_column(ForeignKey(TrainingModel.key))


class LiftingModel(Base):
    __tablename__ = 'lifting'

    sets: Mapped[int] = mapped_column()
    avg_weight: Mapped[float] = mapped_column()
    avg_reps: Mapped[float] = mapped_column()
    avg_pause: Mapped[float] = mapped_column()
    is_stronglift: Mapped[bool] = mapped_column(default=False)

    fk_training: Mapped[int] = mapped_column(ForeignKey(TrainingModel.key))


class LiftingSetModel(Base):
    __tablename__ = 'lifting_set'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)

    fk_lifting: Mapped[int] = mapped_column(ForeignKey(LiftingModel.key))


class StretchingModel(Base):
    __tablename__ = 'stretching'

    seconds: Mapped[float] = mapped_column()
    topic: Mapped[str] = mapped_column()
    fk_training: Mapped[int] = mapped_column(ForeignKey(TrainingModel.key))


class BodyStats(Base):
    __tablename__ = 'body_stats'

    timestamp: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
