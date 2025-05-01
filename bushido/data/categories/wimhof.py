from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column, Session

# project imports
from bushido.data.base_models import AbsKeikoModel, UnitModel


class KeikoModel(AbsKeikoModel):
    __tablename__ = 'wimhof'

    round_nr: Mapped[int] = mapped_column()
    breaths: Mapped[int] = mapped_column()
    retention: Mapped[int] = mapped_column()


class Repository:
    def __init__(self, session: Session):
        self.session = session

    def get_units(self):
        stmt = (select(UnitModel.timestamp,
                       KeikoModel.round_nr,
                       KeikoModel.breaths,
                       KeikoModel.retention)
                .join(KeikoModel, UnitModel.key == KeikoModel.fk_unit)
                .order_by(UnitModel.timestamp.desc()))
        return self.session.execute(stmt).all()
