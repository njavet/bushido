from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import Session

# project imports
from bushido.schema.base import EmojiSpec
from bushido.data.base_tables import MDCategoryTable, MDEmojiTable, UnitTable


class DataManager:
    def __init__(self, db_url) -> None:
        self.engine = create_engine(url=db_url)


    def create_unit_orm(self, unit_spec):
        with (Session(self.engine) as session):
            stmt = (select(MDEmojiTable.key)
                    .where(MDEmojiTable.unit_name == unit_spec.unit_name))
            emoji_key = session.scalar(stmt)
        unit = UnitTable(timestamp=unit_spec.timestamp,
                         payload=' '.join(unit_spec.words),
                         comment=unit_spec.comment,
                         fk_emoji=emoji_key)
        return unit

