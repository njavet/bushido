import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class UnitCategoryTable(Base):
    __tablename__ = "unit_category"

    name: Mapped[str] = mapped_column(unique=True)


class UnitSettingTable(Base):
    __tablename__ = "unit_setting"

    name: Mapped[str] = mapped_column(unique=True)
    category_id: Mapped[int] = mapped_column(ForeignKey(UnitCategoryTable.id))


class UnitTable(Base):
    __abstract__ = True

    comment: Mapped[str | None] = mapped_column()
    log_time: Mapped[datetime.datetime] = mapped_column()

    unit_setting_id: Mapped[int] = mapped_column(ForeignKey(UnitSettingTable.id))
