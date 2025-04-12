from sqlalchemy import create_engine, select, ForeignKey
from sqlalchemy.orm import Session, mapped_column, Mapped

# project imports
from bushido.schema.base import EmojiSpec
from bushido.data.base_tables import (Base,
                                      MDCategoryTable,
                                      MDEmojiTable,
                                      UnitTable)


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

    def load_emojis(self):
        stmt = (select(MDEmojiTable.unit_name,
                       MDEmojiTable.emoji,
                       MDEmojiTable.emoji_text,
                       MDCategoryTable.name,
                       MDEmojiTable.key)
                .join(MDCategoryTable))
        emoji_specs = []
        with Session(self.engine) as session:
            # TODO investigate open session for retrieving keys
            #  -> not bound to a session error
            data = session.execute(stmt).all()
        for item in data:
            emoji_spec = EmojiSpec(emoji=item.emoji,
                                   emoji_text=item.emoji_text,
                                   unit_name=item.unit_name,
                                   category_name=item.name,
                                   key=item.key)
            emoji_specs.append(emoji_spec)
        return emoji_specs

    def create_orm_unit(self, unit_spec):
        with (Session(self.engine) as session):
            stmt = (select(MDEmojiTable.key)
                    .where(MDEmojiTable.emoji == unit_spec.emoji))
            result = session.scalar(stmt)
        unit = UnitTable(timestamp=unit_spec.timestamp,
                         payload=unit_spec.payload,
                         comment=unit_spec.comment,
                         fk_emoji=result.key)
        return unit

    def upload_unit(self, unit_spec, keiko_orm):
        unit = self.create_orm_unit(unit_spec)
        with Session(self.engine) as session:
            session.add(unit)
            session.commit()
            keiko_orm.fk_unit = unit.key
            session.add(keiko_orm)
            session.commit()


class AbsKeikoTable(Base):
    __abstract__ = True
    fk_unit: Mapped[int] = mapped_column(ForeignKey(UnitTable.key))
