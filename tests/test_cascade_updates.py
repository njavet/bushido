import unittest
from sqlalchemy import select
from sqlalchemy.orm import Session


# project imports
from ulib.db import DatabaseManager, db_init
from ulib.db.base import Category


class TestCategoryEmojiCascade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        db_init('sqlite:///bushido.db')
        cls.dbm = DatabaseManager('sqlite:///bushido.db')

    def test_cascade_delete_category(self):
        stmt = select(Category).where(Category.name == 'lifting')
        with Session(self.dbm.engine) as session:
            category = session.scalar(stmt)
            session.delete(category)
            session.commit()


if __name__ == '__main__':
    unittest.main()
