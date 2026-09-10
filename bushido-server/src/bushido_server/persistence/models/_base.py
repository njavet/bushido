import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Spartan(Base):
    """user account"""

    __tablename__ = "spartan"

    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.datetime.now(datetime.UTC)
    )


class UnitTable(Base):
    __abstract__ = True

    name: Mapped[str] = mapped_column()
    log_time: Mapped[datetime.datetime] = mapped_column()
    comment: Mapped[str | None] = mapped_column()

    spartan_id: Mapped[int] = mapped_column(ForeignKey(Spartan.id))
