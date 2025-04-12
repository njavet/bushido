import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# project imports
from bushido.data.base_tables import MDEmojiTable, MDCategoryTable, Base


def db_init(engine):
    Base.metadata.create_all(engine)
    try:
        upload_category_md_data(engine)
        upload_emoji_md_data(engine)
    except IntegrityError:
        # TODO logging
        pass


def upload_category_md_data(engine):
    categories = pd.read_csv('static/csv_files/categories.csv')
    categories = categories.to_dict(orient='records')
    cat_lst = [MDCategoryTable(name=cat['name']) for cat in categories]
    with Session(engine) as session:
        session.add_all(cat_lst)
        session.commit()


def upload_emoji_md_data(engine):
    emojis = pd.read_csv('static/csv_files/emojis.csv')
    emojis = emojis.to_dict(orient='records')
    upload_lst = []
    with Session(engine) as session:
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
