from sqlalchemy.orm import Session
from sqlalchemy import select
from bushido.data.models import MDEmojiTable, MDCategoryTable


class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_category_for_unit(self, unit_name):
        stmt = (select(MDCategoryTable.name)
                .join(MDEmojiTable)
                .where(MDEmojiTable.unit_name == unit_name))
        return self.session.execute(stmt).scalar()
