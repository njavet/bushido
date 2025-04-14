from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from bushido.data.base_models import MDEmojiModel, MDCategoryModel


class EmojiRepository:
    def __init__(self, session: Session):
        self.session = session

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
