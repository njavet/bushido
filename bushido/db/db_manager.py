from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
import pandas as pd

# project imports
from bushido.db.models import Base, Emoji


class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)

    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session

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
        session = self.get_session()
        stmt = select(Emoji)
        pass