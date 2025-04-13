from sqlalchemy import create_engine, select, or_
from sqlalchemy.orm import Session

# project imports
from bushido.data.base_tables import MDCategoryTable, MDEmojiTable, UnitTable


class DataManager:
    def __init__(self, db_url) -> None:
        self.engine = create_engine(url=db_url)

    def receive_all_units(self, unit_name=None, start_t=None, end_t=None):
        stmt = (select(MDEmojiTable.emoji,
                       UnitTable.timestamp,
                       UnitTable.payload,
                       UnitTable.comment)
                .join(UnitTable, MDEmojiTable.key == UnitTable.fk_emoji))
        if unit_name:
            stmt = stmt.where(MDEmojiTable.unit_name == unit_name)
        if start_t:
            start_timestamp = start_t.timestamp()
            stmt = stmt.where(start_timestamp <= UnitTable.timestamp)
        if end_t:
            end_timestamp = end_t.timestamp()
            stmt = stmt.where(UnitTable.timestamp <= end_timestamp)

        with Session(self.engine) as session:
            units = session.execute(stmt).all()
        return units

    def unit_name_to_emoji(self, unit_name):
        stmt = (select(MDEmojiTable.emoji)
                .where(MDEmojiTable.unit_name == unit_name))
        with Session(self.engine) as session:
            emoji = session.scalar(stmt)
        return emoji

    def unit_name_to_category(self, unit_name):
        stmt = (select(MDCategoryTable.name)
                .join(MDEmojiTable)
                .where(MDEmojiTable.unit_name == unit_name))
        with Session(self.engine) as session:
            category = session.execute(stmt).one()
        return category.name

    def emoji_to_unit_name(self, emoji):
        stmt = (select(MDEmojiTable.unit_name)
                .where(or_(MDEmojiTable.emoji == emoji,
                           MDEmojiTable.emoticon == emoji)))
        with Session(self.engine) as session:
            unit_name = session.scalar(stmt)
        return unit_name

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

    def upload_unit(self, unit_spec, keiko_orm):
        unit = self.create_unit_orm(unit_spec)
        with Session(self.engine) as session:
            session.add(unit)
            session.commit()
            keiko_orm.fk_unit = unit.key
            session.add(keiko_orm)
            session.commit()
