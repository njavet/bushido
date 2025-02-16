from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# project imports
from ulib.db.tables import CategoryTable, EmojiTable
from ulib.utils.emojis import create_emoji_dix
from ulib.db.tables.gym import GymUploader
from ulib.db.tables.lifting import LiftingUploader


class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.emoji_dix = create_emoji_dix(self.get_emojis())
        self.uploaders = self.load_uploaders()

    @staticmethod
    def load_retrievers():
        pass

    def load_uploaders(self):
        uploaders = {'gym': GymUploader(self.engine),
                     'lifting': LiftingUploader(self.engine)}
        return uploaders

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
