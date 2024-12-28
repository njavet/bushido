from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import pandas as pd

# project imports
from ulib.db.base import Base, Category, Emoji
from ulib.utils.emojis import create_emoji_dix


class DatabaseManager:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.emoji_dix = create_emoji_dix(self.get_emojis())

    @staticmethod
    def load_retrievers():
        pass

    @staticmethod
    def load_uploaders():
        pass

    def init_db(self):
        self.init_tables()
        self.upload_category_data()
        self.upload_emoji_data()

    def init_tables(self, tables=None):
        if tables is not None:
            tables = [table.__table__ for table in tables]
            Base.metadata.create_all(self.engine, tables=tables)
        else:
            Base.metadata.create_all(self.engine)

    def drop_tables(self, tables=None):
        if tables is not None:
            tables = [table.__table__ for table in tables]
            Base.metadata.drop_all(self.engine, tables=tables)
        else:
            Base.metadata.drop_all(self.engine)

    def upload_category_data(self):
        categories = pd.read_csv('ulib/resources/categories.csv')
        categories.to_sql('category',
                          self.engine,
                          index=False,
                          if_exists='append')

    def upload_emoji_data(self):
        upload_lst = []
        with Session(self.engine) as session:
            categories = session.scalars(select(Category)).all()
            cat_map = {cat.name: cat.key for cat in categories}
            emojis_df = pd.read_csv('ulib/resources/emojis.csv')
            emojis = emojis_df.to_dict(orient='records')
            for emoji_data in emojis:
                cat_key = cat_map[emoji_data['category']]
                emoji = Emoji(emoji_base=emoji_data['emoji_base'],
                              emoji_ext=emoji_data['emoji_ext'],
                              emoji_name=emoji_data['emoji_name'],
                              unit_name=emoji_data['unit_name'],
                              category=cat_key)
                upload_lst.append(emoji)
            session.add_all(upload_lst)
            session.commit()

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
