import unittest
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session


# project imports
from bushido.db.base_tables import MDCategoryTable
from bushido.db.db_init import db_init


class TestCategoryEmojiCascade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///:memory:')
        db_init(engine)
        cls.engine = engine

    def test_cascade_delete_category(self):
        stmt = select(MDCategoryTable).where(MDCategoryTable.name == 'lifting')
        with Session(self.engine) as session:
            category = session.scalar(stmt)
            session.delete(category)
            session.commit()


if __name__ == '__main__':
    unittest.main()
