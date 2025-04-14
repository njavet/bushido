from sqlalchemy import select, or_
from sqlalchemy.orm import Session
# project imports
from bushido.data.models import UnitTable, MDEmojiTable, MDCategoryTable


class UnitRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        stmt = select(MDEmojiTable.emoji, MDEmojiTable.unit_name)
        return self.session.execute(stmt).all()

    def get_emoji_for_unit(self, unit_name: str):
        stmt = select(MDEmojiTable.emoji).where(MDEmojiTable.unit_name == unit_name)
        return self.session.scalar(stmt)

    def get_emoji_key_by_unit(self, unit_name: str):
        stmt = (select(MDEmojiTable.key)
                .where(MDEmojiTable.unit_name == unit_name))
        emoji_key = self.session.scalar(stmt)
        return emoji_key

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

    def get_category_for_unit(self, unit_name):
        stmt = (select(MDCategoryTable.name)
                .join(MDEmojiTable)
                .where(MDEmojiTable.unit_name == unit_name))
        return self.session.execute(stmt).scalar()

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
