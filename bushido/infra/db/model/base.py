from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class Unit(Base):
    __abstract__ = True

    name: Mapped[str] = mapped_column()
    comment: Mapped[str | None] = mapped_column()


class Subunit(Base):
    __abstract__ = True
    fk_unit: Mapped[int] = mapped_column()
