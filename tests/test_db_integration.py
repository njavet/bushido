import unittest
import peewee as pw

# project imports
from bushido.keikolib.db import Unit, Message


test_db = pw.SqliteDatabase(':memory:')
models = [Unit, Message]


class TestInitDatabaseIntegration(unittest.TestCase):
    def setUp(self):
        test_db.bind(models)
        test_db.connect()
        test_db.create_tables(models)

    def tearDown(self):
        test_db.drop_tables(models)
        test_db.close()

    def test_init_database(self):
        self.assertTrue(Unit.table_exists())
        self.assertTrue(Message.table_exists())
        self.assertFalse(test_db.is_closed())


if __name__ == '__main__':
    unittest.main()
