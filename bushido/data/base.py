import pandas as pd
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# project imports
from bushido.data.db import MDEmojiTable, MDCategoryTable, UnitTable, Base
from bushido.model.base import EmojiSpec


class DatabaseManager:
    def __init__(self, db_url) -> None:
        self.engine = create_engine(url=db_url)
        self.init_db()

    def load_emojis(self):
        stmt = (select(MDEmojiTable.unit_name,
                       MDEmojiTable.emoji,
                       MDEmojiTable.emoji_text,
                       MDCategoryTable.name,
                       MDEmojiTable.key)
                .join(MDCategoryTable))
        emoji2emoji_spec = {}
        emoji_text2emoji = {}
        with Session(self.engine) as session:
            # TODO investigate open session for retrieving keys
            #  -> not bound to a session error
            data = session.execute(stmt).all()
        for item in data:
            emoji_spec = EmojiSpec(emoji=item.emoji,
                                   emoji_text=item.emoji_text,
                                   unit_name=item.unit_name,
                                   category_name=item.category_name,
                                   key=item.key)
            emoji2emoji_spec[item.emoji] = emoji_spec
            emoji_text2emoji[item.emoji_text] = item.emoji
        return emoji2emoji_spec, emoji_text2emoji

    def retrieve_all_units(self):
        stmt = (select(MDEmojiTable.emoji,
                       UnitTable.timestamp,
                       UnitTable.payload,
                       UnitTable.comment)
                .join(UnitTable)
                ).order_by(UnitTable.timestamp.desc())
        with Session(self.engine) as session:
            units = session.execute(stmt).all()
        return units

    def init_db(self):
        Base.metadata.create_all(self.engine)
        try:
            self.upload_category_md_data()
            self.upload_emoji_md_data()
        except IntegrityError:
            # TODO logging
            pass

    def upload_category_md_data(self):
        categories = pd.read_csv('bushido/static/csv_files/categories.csv')
        categories = categories.to_dict(orient='records')
        cat_lst = [MDCategoryTable(name=cat['name']) for cat in categories]
        with Session(self.engine) as session:
            session.add_all(cat_lst)
            session.commit()

    def upload_emoji_md_data(self):
        emojis = pd.read_csv('bushido/static/csv_files/emojis.csv')
        emojis = emojis.to_dict(orient='records')
        upload_lst = []
        with Session(self.engine) as session:
            categories = session.scalars(select(MDCategoryTable)).all()
            cat_map = {cat.name: cat.key for cat in categories}
            for emoji_data in emojis:
                cat_key = cat_map[emoji_data['category_name']]
                emoji = MDEmojiTable(unit_name=emoji_data['unit_name'],
                                     emoji_name=emoji_data['emoji_name'],
                                     emoji_text=emoji_data['emoji_text'],
                                     emoji=emoji_data['emoji'],
                                     fk_category=cat_key)
                upload_lst.append(emoji)
        session.add_all(upload_lst)
        session.commit()
