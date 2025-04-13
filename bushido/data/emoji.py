from sqlalchemy.orm import Session
from sqlalchemy import select
from bushido.data.base_tables import MDEmojiTable


class EmojiRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        stmt = select(MDEmojiTable.emoji, MDEmojiTable.unit_name)
        return self.session.execute(stmt).all()

    def get_emoji_for_unit(self, unit_name: str):
        stmt = select(MDEmojiTable.emoji).where(MDEmojiTable.unit_name == unit_name)
        return self.session.scalar(stmt)
