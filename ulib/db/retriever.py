from sqlalchemy import select
from sqlalchemy.orm import Session

# project imports
from .models import Emoji, Category


class Retriever:
    def __init__(self, engine):
        self.engine = engine

    def get_emojis(self):
        stmt = (select(Emoji.emoji_base,
                       Emoji.emoji_ext,
                       Category.name,
                       Emoji.unit_name,
                       Emoji.key)
                .join(Emoji))
        with Session(self.engine) as session:
            emojis = session.execute(stmt).all()
        return emojis
