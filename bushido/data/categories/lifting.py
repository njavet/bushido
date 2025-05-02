from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column, Session

# project imports
from bushido.data.base_models import AbsKeikoModel, UnitModel, MDEmojiModel


class KeikoModel(AbsKeikoModel):
    __tablename__ = 'lifting'

    set_nr: Mapped[int] = mapped_column()
    weight: Mapped[float] = mapped_column()
    reps: Mapped[float] = mapped_column()
    pause: Mapped[int] = mapped_column(default=0)


class Repository:
    def __init__(self, session: Session):
        self.session = session

    def get_sets(self):
        stmt = (select(MDEmojiModel.unit_name,
                       UnitModel.timestamp,
                       KeikoModel.set_nr,
                       KeikoModel.weight,
                       KeikoModel.reps,
                       KeikoModel.pause)
                .join(MDEmojiModel, MDEmojiModel.key == UnitModel.fk_emoji)
                .join(KeikoModel, UnitModel.key == KeikoModel.fk_unit)
                .order_by(UnitModel.timestamp.desc()))
        return self.session.execute(stmt).all()

    def get_sets_from_unit_name(self, unit_name):
        stmt = (select(UnitModel.timestamp,
                       KeikoModel.set_nr,
                       KeikoModel.weight,
                       KeikoModel.reps,
                       KeikoModel.pause)
                .join(MDEmojiModel, MDEmojiModel.key == UnitModel.fk_emoji)
                .join(KeikoModel, UnitModel.key == KeikoModel.fk_unit)
                .where(MDEmojiModel.unit_name == unit_name)
                .order_by(UnitModel.timestamp.desc()))
        return self.session.execute(stmt).all()
