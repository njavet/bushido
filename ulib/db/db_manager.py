from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# project imports
from ulib.db.tables.gym import GymUploader
from ulib.db.tables.lifting import LiftingUploader


class DBManager:
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

