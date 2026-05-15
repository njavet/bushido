import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class UnitTable(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    emoji: Mapped[str] = mapped_column()
    comment: Mapped[str | None] = mapped_column()
    log_time: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(datetime.timezone.utc)
    )


class Subunit(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
