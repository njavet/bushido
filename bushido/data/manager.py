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

    def upload_unit(self, unit_spec, keiko):
        unit = self.create_unit_orm(unit_spec)
        with Session(self.engine) as session:
            session.add(unit)
            session.commit()
            if isinstance(keiko, list):
                for keiko_orm in keiko:
                    keiko_orm.fk_unit = unit.key
                    session.add(keiko_orm)
            else:
                keiko.fk_unit = unit.key
                session.add(keiko)
            session.commit()
