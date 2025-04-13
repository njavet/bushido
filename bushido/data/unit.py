from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from bushido.data.base_tables import UnitTable, MDEmojiTable


class UnitRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_units(self, unit_name=None, start_t=None, end_t=None):
        stmt = (select(MDEmojiTable.emoji,
                       UnitTable.timestamp,
                       UnitTable.payload,
                       UnitTable.comment)
                .join(UnitTable, MDEmojiTable.key == UnitTable.fk_emoji))

        if unit_name:
            stmt = stmt.where(MDEmojiTable.unit_name == unit_name)
        if start_t:
            stmt = stmt.where(start_t.timestamp() <= UnitTable.timestamp)
        if end_t:
            stmt = stmt.where(UnitTable.timestamp <= end_t.timestamp())

        return self.session.execute(stmt).all()

    def get_unit_name_for_emoji(self, emoji: str):
        stmt = (select(MDEmojiTable.unit_name)
                .where(or_(MDEmojiTable.emoji == emoji,
                           MDEmojiTable.emoticon == emoji)))
        return self.session.scalar(stmt)

    def save_unit_and_keiko(self, unit, keiko):
        self.session.add(unit)
        self.session.commit()

        if isinstance(keiko, list):
            for k in keiko:
                k.fk_unit = unit.key
            self.session.add_all(keiko)
        else:
            keiko.fk_unit = unit.key
            self.session.add(keiko)
        self.session.commit()
