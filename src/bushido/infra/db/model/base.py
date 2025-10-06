import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Spartan(Base):
    __tablename__ = "spartan"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    birth_date: Mapped[datetime.datetime | None] = mapped_column()


class BushidoDay(Base):
    __tablename__ = "bushido_day"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[datetime.date] = mapped_column()
    start_t: Mapped[datetime.time] = mapped_column(default=datetime.time(4, 0))
    end_t: Mapped[datetime.time] = mapped_column(default=datetime.time(3, 59))


class Unit(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    comment: Mapped[str | None] = mapped_column()
    log_time: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.now(datetime.timezone.utc)
    )
