import unittest
from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session


# project imports
from bushido.data.base_models import MDCategoryModel
from bushido.data.db_init import db_init


class TestCategoryEmojiCascade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = db_init('sqlite:///:memory:')

    def test_cascade_delete_category(self):
        stmt = select(MDCategoryModel).where(MDCategoryModel.name == 'lifting')
        with Session(self.engine) as session:
            category = session.scalar(stmt)
            session.delete(category)
            session.commit()


if __name__ == '__main__':
    unittest.main()
