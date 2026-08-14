import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class UnitSettingTable(Base):
    __tablename__ = "unit_setting"

    name: Mapped[str] = mapped_column()
    category: Mapped[str] = mapped_column()


class UnitTable(Base):
    __abstract__ = True

    name: Mapped[str] = mapped_column()
    comment: Mapped[str | None] = mapped_column()
    log_time: Mapped[datetime.datetime] = mapped_column()
