from sqlalchemy import select
from sqlalchemy.orm import Session

# project imports
from ulib.db.tables.base import EmojiTable, CategoryTable
from ulib.schemas.base import Emoji, Unit


class BaseRetriever:
    def __init__(self, engine):
        self.engine = engine

    def get_emojis(self):
        stmt = (select(EmojiTable.base_emoji,
                       EmojiTable.ext_emoji,
                       CategoryTable.name,
                       EmojiTable.unit_name,
                       EmojiTable.key)
                .join(CategoryTable))
        with Session(self.engine) as session:
            emojis = session.execute(stmt).all()
        return emojis
