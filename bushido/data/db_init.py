from typing import Optional
import pandas as pd
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

# project imports
from bushido.data.db import (MDCategoryTable,
                                    MDEmojiTable,
                                    Base)
from bushido.model.base import EmojiProcessor


def db_init(engine):
    Base.metadata.create_all(engine)
    try:
        upload_category_md_data(engine)
        upload_emoji_md_data(engine)
    except IntegrityError:
        # TODO logging
        pass


def upload_category_md_data(engine):
    categories = pd.read_csv('bushido/static/csv_files/categories.csv')
    categories = categories.to_dict(orient='records')
    cat_lst = [MDCategoryTable(name=cat['name']) for cat in categories]
    with Session(engine) as session:
        session.add_all(cat_lst)
        session.commit()


def upload_emoji_md_data(engine):
    emojis = pd.read_csv('bushido/static/csv_files/emojis.csv')
    emojis = emojis.to_dict(orient='records')
    upload_lst = []
    with Session(engine) as session:
        categories = session.scalars(select(MDCategoryTable)).all()
        cat_map = {cat.name: cat.key for cat in categories}
        for emoji_data in emojis:
            cat_key = cat_map[emoji_data['category_name']]
            emoji = MDEmojiTable(base_emoji=emoji_data['base_emoji'],
                                 ext_emoji=emoji_data['ext_emoji'],
                                 emoji_name=emoji_data['emoji_name'],
                                 unit_name=emoji_data['unit_name'],
                                 fk_category=cat_key)
            upload_lst.append(emoji)
    session.add_all(upload_lst)
    session.commit()


def get_emojis(engine):
    stmt = (select(MDEmojiTable.base_emoji,
                   MDEmojiTable.ext_emoji,
                   MDCategoryTable.name,
                   MDEmojiTable.unit_name,
                   MDEmojiTable.key)
            .join(MDCategoryTable))
    emoji_lst = []
    with Session(engine) as session:
        # TODO investigate open session for retrieving keys
        #  -> not bound to a session error
        data = session.execute(stmt).all()
    for item in data:
        byte_seq = item.base_emoji.encode('utf-8')
        base_emoji = byte_seq.decode('unicode_escape')
        if item.ext_emoji is None:
            emoji = base_emoji
        else:
            bs = (item.base_emoji + item.ext_emoji).encode('utf-8')
            emoji = bs.decode('unicode_escape')
        emoji_spec = EmojiProcessor(base_emoji=base_emoji,
                                    emoji=emoji,
                                    category_name=item.name,
                                    unit_name=item.unit_name,
                                    key=item.key)
        emoji_lst.append(emoji_spec)
    return emoji_lst
