from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
import pandas as pd

# project imports
from ulib.db.tables import Base, CategoryTable, EmojiTable
from ulib.schemas.base import Category, Emoji


def db_init(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    cats = upload_category_data(engine)


def upload_category_data(engine):
    categories = pd.read_csv('ulib/resources/categories.csv').to_dict(orient='list')
    lst = []
    for name in categories.values():
        cat = CategoryTable(name=name)
        lst.append(cat)
    with Session(engine) as session:
        session.add_all(lst)
        session.commit()
    return lst


def upload_emoji_data(engine):
    upload_lst = []
    with Session(engine) as session:
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
