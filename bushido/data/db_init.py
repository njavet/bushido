import pandas as pd
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

# project imports
from bushido.conf import MASTER_DATA_DIR
from bushido.utils.emojis import decode
from bushido.data.models import MDEmojiTable, MDCategoryTable, Base


def db_init(engine):
    Base.metadata.create_all(engine)
    try:
        upload_category_md_data(engine)
        upload_emoji_md_data(engine)
    except IntegrityError:
        # TODO logging
        pass


def upload_category_md_data(engine, categories_csv: str = 'categories.csv'):
    categories_path = MASTER_DATA_DIR.joinpath(categories_csv)
    categories = pd.read_csv(categories_path)
    categories = categories.to_dict(orient='records')
    cat_lst = [MDCategoryTable(name=cat['name']) for cat in categories]
    with Session(engine) as session:
        session.add_all(cat_lst)
        session.commit()


def upload_emoji_md_data(engine, emojis_csv: str = 'emojis.csv'):
    emojis_path = MASTER_DATA_DIR.joinpath(emojis_csv)
    df = pd.read_csv(emojis_path)
    df = decode(df)
    emojis = df.to_dict(orient='records')
    upload_lst = []
    with Session(engine) as session:
        categories = session.scalars(select(MDCategoryTable)).all()
        cat_map = {cat.name: cat.key for cat in categories}
        for emoji_data in emojis:
            cat_key = cat_map[emoji_data['category_name']]
            emoji_orm = MDEmojiTable(unit_name=emoji_data['unit_name'],
                                     emoji_name=emoji_data['emoji_name'],
                                     emoticon=emoji_data['emoticon'],
                                     emoji=emoji_data['emoji'],
                                     fk_category=cat_key)
            upload_lst.append(emoji_orm)
    session.add_all(upload_lst)
    session.commit()
