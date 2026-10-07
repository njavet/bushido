import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from citadel.persistence.models import (
    BarbellUnitTable,
    Base,
    ChronoUnitTable,
    LiftingUnitTable,
    LogUnitTable,
    MartialArtsUnitTable,
    RopeSkipUnitTable,
    RunningUnitTable,
    SwimmingUnitTable,
    WimhofUnitTable,
    WorkUnitTable,
)


class Spartan(Base):
    __tablename__ = "spartan"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.UTC)
    )


class UnitTable(Base):
    __tablename__ = "unit"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    spartan_id: Mapped[int] = mapped_column(ForeignKey(Spartan.id))

    unit_type: Mapped[str] = mapped_column()
    name: Mapped[str] = mapped_column()
    log_time: Mapped[datetime.datetime] = mapped_column()
    comment: Mapped[str | None] = mapped_column()

    barbell: Mapped[BarbellUnitTable | None] = relationship(
        back_populates="unit",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    swimming: Mapped[SwimmingUnitTable | None] = relationship(
        back_populates="unit",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    running: Mapped[RunningUnitTable | None] = relationship(
        back_populates="unit",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    skipping: Mapped[RopeSkipUnitTable | None] = relationship(
        back_populates="unit",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    chrono: Mapped[ChronoUnitTable | None] = relationship(
        back_populates="unit",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    lifting: Mapped[LiftingUnitTable | None] = relationship(
        back_populates="unit",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    log: Mapped[LogUnitTable | None] = relationship(
        back_populates="unit",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    martial_arts: Mapped[MartialArtsUnitTable | None] = relationship(
        back_populates="unit",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    wimhof: Mapped[WimhofUnitTable | None] = relationship(
        back_populates="unit",
        cascade="all, delete-orphan",
        single_parent=True,
    )
    work: Mapped[WorkUnitTable | None] = relationship(
        back_populates="unit",
        cascade="all, delete-orphan",
        single_parent=True,
    )
