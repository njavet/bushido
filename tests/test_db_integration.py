import unittest

# project imports
from bushido.db import DatabaseManager


class TestBaseDataIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dbm = DatabaseManager('sqlite:///:memory:')
        dbm.init_tables()
        dbm.upload_category_data()
        dbm.upload_emoji_data()
        cls.dbm = dbm

    def test_init_database(self):
        pass


if __name__ == '__main__':
    unittest.main()
