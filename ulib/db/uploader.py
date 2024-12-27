from sqlalchemy import select
from sqlalchemy.orm import Session
import pandas as pd

# project imports
from .models import Emoji, Category, Unit, Message


class Uploader:
    def __init__(self, engine):
        self.engine = engine

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

    def upload_unit(self, unix_timestamp, emoji_key):
        unit = Unit(unix_timestamp=unix_timestamp,
                    emoji=emoji_key)
        with Session(self.engine) as session:
            session.add(unit)
            session.commit()
        return unit.key

    def upload_message(self, payload, comment, unit_key):
        message = Message(payload=payload,
                          comment=comment,
                          unit=unit_key)
        with Session(self.engine) as session:
            session.add(message)
            session.commit()

    def upload_keiko(self, attrs, unit_key, tablename):
        pass