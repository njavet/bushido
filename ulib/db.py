from typing import Optional
import pandas as pd
from sqlalchemy import ForeignKey, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import (DeclarativeBase,
                            Mapped,
                            mapped_column,
                            Session)


class Base(DeclarativeBase):
    __abstract__ = True
    key: Mapped[int] = mapped_column(primary_key=True)


class MDCategoryTable(Base):
    __tablename__ = 'md_category'
    name: Mapped[str] = mapped_column(unique=True)


class MDEmojiTable(Base):
    __tablename__ = 'md_emoji'
    base_emoji: Mapped[str] = mapped_column(unique=True)
    ext_emoji: Mapped[Optional[str]] = mapped_column()
    emoji_name: Mapped[str] = mapped_column(unique=True)
    unit_name: Mapped[str] = mapped_column(unique=True)
    fk_category: Mapped[int] = mapped_column(ForeignKey(MDCategoryTable.key))


class UnitTable(Base):
    __tablename__ = 'unit'
    timestamp: Mapped[float] = mapped_column()
    payload: Mapped[str] = mapped_column()
    comment: Mapped[Optional[str]] = mapped_column()
    fk_emoji: Mapped[int] = mapped_column(ForeignKey(MDEmojiTable.key))


def init_db(engine):
    Base.metadata.create_all(engine)
    try:
        upload_category_data(engine)
        upload_emoji_data(engine)
    except IntegrityError:
        # TODO logging
        pass


def upload_category_data(engine):
    categories = (pd
                  .read_csv('ulib/resources/categories.csv')
                  .to_dict(orient='records'))
    cat_lst = [MDCategoryTable(name=cat['name']) for cat in categories]
    with Session(engine) as session:
        session.add_all(cat_lst)
        session.commit()


def upload_emoji_data(engine):
    upload_lst = []
    with Session(engine) as session:
        categories = session.scalars(select(MDCategoryTable)).all()
        cat_map = {cat.name: cat.key for cat in categories}
        emojis_df = pd.read_csv('ulib/resources/emojis.csv')
        emojis = emojis_df.to_dict(orient='records')
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
