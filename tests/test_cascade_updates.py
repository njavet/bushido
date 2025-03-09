import unittest
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session


# project imports
from ulib.db import MDCategoryTable, init_db


class TestCategoryEmojiCascade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        engine = create_engine('sqlite:///:memory:')
        init_db(engine)
        cls.engine = engine

    def test_cascade_delete_category(self):
        stmt = select(MDCategoryTable).where(MDCategoryTable.name == 'lifting')
        with Session(self.engine) as session:
            category = session.scalar(stmt)
            session.delete(category)
            session.commit()


if __name__ == '__main__':
    unittest.main()
