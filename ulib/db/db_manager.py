from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# project imports
from ulib.db.tables import CategoryTable, EmojiTable
from ulib.db.db_init import db_init
from ulib.utils.emojis import create_emoji_dix
from ulib.db.tables.gym import GymUploader
from ulib.db.tables.lifting import LiftingUploader


class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        db_init(self.engine)
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
        stmt = (select(EmojiTable.emoji_base,
                       EmojiTable.emoji_ext,
                       CategoryTable.name,
                       EmojiTable.unit_name,
                       EmojiTable.key)
                .join(CategoryTable))
        with Session(self.engine) as session:
            emojis = session.execute(stmt).all()
        return emojis
