import unittest
from sqlalchemy import select
from sqlalchemy.orm import Session


# project imports
from ulib.db import DatabaseManager
from ulib.db.base import Category, Emoji, Unit


class TestCategoryEmojiCascade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dbm = DatabaseManager('sqlite:///bushido.db')
        dbm.init_tables([Category, Emoji, Unit])
        dbm.upload_category_data()
        dbm.upload_emoji_data()
        cls.dbm = dbm

    def test_cascade_delete_category(self):
        stmt = select(Category).where(Category.name == 'lifting')
        with Session(self.dbm.engine) as session:
            category = session.scalar(stmt)
            session.delete(category)
            session.commit()


if __name__ == '__main__':
    unittest.main()
