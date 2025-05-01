from sqlalchemy import select, or_
from sqlalchemy.orm import Session

# project imports
from bushido.data.base_models import MDEmojiModel, MDCategoryModel, UnitModel


class Repository:
    def __init__(self, session: Session):
        self.session = session

    def get_master_data(self):
        stmt = (select(MDCategoryModel.name,
                       MDEmojiModel.emoji,
                       MDEmojiModel.unit_name)
                .join(MDEmojiModel,
                      MDCategoryModel.key == MDEmojiModel.fk_category))
        return self.session.execute(stmt).all()

    def get_all_categories(self):
        stmt = select(MDCategoryModel.name)
        return self.session.execute(stmt).all()

    def get_all_emojis(self):
        stmt = select(MDEmojiModel.emoji, MDEmojiModel.unit_name)
        return self.session.execute(stmt).all()

    def get_emoji_for_unit(self, unit_name: str):
        stmt = select(MDEmojiModel.emoji).where(MDEmojiModel.unit_name == unit_name)
        return self.session.scalar(stmt)

    def get_emoji_key_by_unit(self, unit_name: str):
        stmt = (select(MDEmojiModel.key)
                .where(MDEmojiModel.unit_name == unit_name))
        emoji_key = self.session.scalar(stmt)
        return emoji_key

    def get_unit_name_for_emoji(self, emoji: str):
        stmt = (select(MDEmojiModel.unit_name)
                .where(or_(MDEmojiModel.emoji == emoji,
                           MDEmojiModel.emoticon == emoji)))
        return self.session.scalar(stmt)

    def get_category_for_unit(self, unit_name):
        stmt = (select(MDCategoryModel.name)
                .join(MDEmojiModel)
                .where(MDEmojiModel.unit_name == unit_name))
        return self.session.execute(stmt).scalar()

    def get_units(self,
                  category=None,
                  unit_name=None,
                  start_dt=None,
                  end_dt=None):
        stmt = (select(MDEmojiModel.emoji,
                       MDEmojiModel.unit_name,
                       UnitModel.timestamp,
                       UnitModel.payload,
                       UnitModel.comment)
                .join(UnitModel, MDEmojiModel.key == UnitModel.fk_emoji)
                .order_by(UnitModel.timestamp.desc()))
        if category:
            stmt = stmt.where(MDCategoryModel.name == category)
        if unit_name:
            stmt = stmt.where(MDEmojiModel.unit_name == unit_name)
        if start_dt:
            stmt = stmt.where(start_dt.timestamp() <= UnitModel.timestamp)
        if end_dt:
            stmt = stmt.where(UnitModel.timestamp <= end_dt.timestamp())
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
