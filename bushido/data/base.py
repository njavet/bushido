from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from collections import defaultdict

# project imports
from bushido.data.db import MDEmojiTable, MDCategoryTable, UnitTable
from bushido.model.base import EmojiSpec
from bushido.utils.emojis import combine_emoji
from bushido.utils.dt_functions import (get_bushido_date_from_datetime,
                                        get_datetime_from_timestamp)


class DatabaseManager:
    def __init__(self, db_url) -> None:
        self.engine = create_engine(url=db_url)

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


    def load_emojis(self):
        for emoji_spec in get_emojis(self.engine):
            self.emoji2spec[emoji_spec.base_emoji] = emoji_spec
            self.emoji2spec[emoji_spec.emoji] = emoji_spec


    def get_date2units(self) -> dict:
        stmt = (select(MDEmojiTable.base_emoji,
                       MDEmojiTable.ext_emoji,
                       UnitTable.timestamp,
                       UnitTable.payload,
                       UnitTable.comment)
                .join(UnitTable)
                ).order_by(UnitTable.timestamp.desc())
        with Session(self.engine) as session:
            results = session.execute(stmt).all()
        dix = defaultdict(list)
        for result in results:
            dt = get_datetime_from_timestamp(result.timestamp)
            bushido_date = get_bushido_date_from_datetime(dt)
            emoji = combine_emoji(result.base_emoji, result.ext_emoji)
            ud = UnitDisplay(bushido_date=bushido_date,
                             day_time=dt.time(),
                             emoji=emoji,
                             payload=result.payload,
                             comment=result.comment)
            dix[bushido_date].append(ud)
        return dix