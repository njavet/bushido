from abc import ABC
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# project import
from ulib.db import Base, UnitTable


class AbsCategory(ABC):
    def __init__(self, name, engine):
        self.name = name
        self.engine = engine
        self.keiko = None


class AbsProcessor(ABC):
    def __init__(self, engine):
        self.engine = engine
        self.attrs = None

    def process_unit(self, timestamp, words, comment, emoji_key):
        self.process_keiko(words)
        unit = UnitTable(timestamp=timestamp,
                         payload=' '.join(words),
                         comment=comment,
                         fk_emoji=emoji_key)

    def process_keiko(self, words):
        raise NotImplementedError


class KeikoTable(Base):
    __abstract__ = True
    fk_unit: Mapped[int] = mapped_column(ForeignKey(UnitTable.key))



    def get_emojis(self):
        stmt = (select(MDEmojiTable.base_emoji,
                       MDEmojiTable.ext_emoji,
                       MDCategoryTable.name,
                       MDEmojiTable.unit_name,
                       MDEmojiTable.key)
                .join(MDCategoryTable))
        emoji_lst = []
        with Session(self.engine) as session:
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
                emoji_spec = Emoji(base_emoji=base_emoji,
                                   emoji=emoji,
                                   category_name=item.name,
                                   unit_name=item.unit_name,
                                   key=item.key)
                emoji_lst.append(emoji_spec)
        return emoji_lst

    def create_emoji_dict(self) -> dict:
        emoji_specs = self.get_emojis()
        dix = {}
        for emoji_spec in emoji_specs:
            dix[emoji_spec.base_emoji] = emoji_spec
            dix[emoji_spec.emoji] = emoji_spec
        return dix

