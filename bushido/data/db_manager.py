import importlib
from pathlib import Path
from collections import defaultdict
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

# project imports
from bushido.data.db_init import db_init, get_emojis
from bushido.data.db import MDEmojiTable, UnitTable
from bushido.model.base import UnitDisplay
from bushido.utils.emojis import combine_emoji
from bushido.utils.dt_functions import (get_bushido_date_from_datetime,
                                        get_datetime_from_timestamp)


class DatabaseManager:
    def __init__(self, db_url) -> None:
        self.engine = create_engine(url=db_url)
        self.cn2proc = {}
        self.cn2cat = {}
        self.emoji2spec = {}
        # sequence important because of Base table
        self.load_categories()
        #db_init(self.engine)
        self.load_emojis()

    def load_categories(self):
        categories = Path('bushido/data/categories')
        for module_path in categories.rglob('[a-z]*.py'):
            module_name = module_path.stem
            import_path = '.'.join(module_path.parts[0:-1]) + '.' + module_name
            module = importlib.import_module(import_path)
            self.cn2cat[module_name] = module.Category(self.engine)
            self.cn2proc[module_name] = module.Processor(self.engine)

    def load_emojis(self):
        for emoji_spec in get_emojis(self.engine):
            self.emoji2spec[emoji_spec.base_emoji] = emoji_spec
            self.emoji2spec[emoji_spec.emoji] = emoji_spec

    def process_input(self, timestamp, input_str):
        try:
            emoji, words, comment = self._preprocess_string(input_str)
        except ValueError as err:
            return str(err)

        try:
            emoji_spec = self.emoji2spec[emoji]
        except KeyError:
            return 'Unknown emoji'

        try:
            self.cn2proc[emoji_spec.category_name].process_unit(
                timestamp, words, comment, emoji_spec.key
            )
        except ValueError:
            return 'parsing error'

    @staticmethod
    def _preprocess_string(input_str: str):
        parts = input_str.split('//', 1)
        emoji_payload = parts[0]
        if not emoji_payload:
            raise ValueError('Empty payload')
        if len(parts) > 1 and parts[1]:
            comment = parts[1].strip()
        else:
            comment = None
        all_words = emoji_payload.split()
        emoji = all_words[0]
        words = all_words[1:]
        return emoji, words, comment

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
