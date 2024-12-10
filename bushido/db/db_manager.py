from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import pandas as pd

# project imports
from bushido.db.models import Base, Emoji


class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)

    def init_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

    def upload_master_data(self):
        categories = pd.read_csv('bushido/static/master_data/categories.csv')
        categories.to_sql('category', self.engine, index=False, if_exists='append')
        emojis = pd.read_csv('bushido/static/master_data/emojis.csv')
        emojis.to_sql('emoji', self.engine, index=False, if_exists='append')

    def download_emoji_to_dict(self):
        stmt = select(Emoji)
        pass


def prepare_emojis():
    emojis = pd.read_csv('bushido/static/master_data/emojis.csv')
    emojis['emoji_ext'] = emojis['emoji_ext'].fillna('')
    emojis['emoji'] = emojis['emoji_base'] + emojis['emoji_ext']
    emojis['emoji'] = emojis['emoji'].apply(
        lambda x: x.encode('utf-8').decode('unicode_escape')
    )
    return emojis

