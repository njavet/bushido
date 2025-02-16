import unittest
from sqlalchemy import select
from sqlalchemy.orm import Session


# project imports
from ulib.db.db_manager import DatabaseManager
from ulib.db.tables import CategoryTable


class TestCategoryEmojiCascade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dbm = DatabaseManager('sqlite:///:memory:')

    def test_cascade_delete_category(self):
        stmt = select(CategoryTable).where(CategoryTable.name == 'lifting')
        with Session(self.dbm.engine) as session:
            category = session.scalar(stmt)
            session.delete(category)
            session.commit()


if __name__ == '__main__':
    unittest.main()
