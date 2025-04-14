from sqlalchemy import select
from sqlalchemy.orm import Session
from bushido.data.base_models import MDEmojiModel, UnitModel


class UnitRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_units(self, unit_name=None, start_t=None, end_t=None):
        stmt = (select(MDEmojiModel.emoji,
                       UnitModel.timestamp,
                       UnitModel.payload,
                       UnitModel.comment)
                .join(UnitModel, MDEmojiModel.key == UnitModel.fk_emoji))

        if unit_name:
            stmt = stmt.where(MDEmojiModel.unit_name == unit_name)
        if start_t:
            stmt = stmt.where(start_t.timestamp() <= UnitModel.timestamp)
        if end_t:
            stmt = stmt.where(UnitModel.timestamp <= end_t.timestamp())

        return self.session.execute(stmt).all()

    def save_unit(self, unit):
        self.session.add(unit)
        self.session.commit()
        return unit.key

    def save_keiko(self, unit_key, keiko):
        if isinstance(keiko, list):
            for k in keiko:
                k.fk_unit = unit_key
            self.session.add_all(keiko)
        else:
            keiko.fk_unit = unit_key
            self.session.add(keiko)
        self.session.commit()
