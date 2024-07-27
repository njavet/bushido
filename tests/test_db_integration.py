import unittest
import peewee as pw

# project imports
from bushido.db import Budoka, Unit, Message, add_budoka, get_me


test_db = pw.SqliteDatabase(':memory:')
models = [Budoka,
          Unit,
          Message]


class TestInitDatabaseIntegration(unittest.TestCase):
    def setUp(self):
        test_db.bind(models)
        test_db.connect()
        test_db.create_tables(models)

    def tearDown(self):
        test_db.drop_tables(models)
        test_db.close()

    def test_init_database(self):
        self.assertTrue(Budoka.table_exists())
        self.assertTrue(Unit.table_exists())
        self.assertTrue(Message.table_exists())
        self.assertFalse(test_db.is_closed())

    def test_add_budoka(self):
        budoka = add_budoka(0, 'Nietzsche')
        self.assertIsNotNone(budoka)

    def test_add_budoka_duplicate(self):
        budoka0 = add_budoka(0, 'Kant')
        self.assertIsNotNone(budoka0)
        budoka1 = add_budoka(0, 'Schopenhauer', False)
        self.assertIsNone(budoka1)

    def test_get_me_exists(self):
        add_budoka(0, 'Platon', True)
        budoka = get_me()
        self.assertIsNotNone(budoka)

    def test_get_me_does_not_exist(self):
        budoka = get_me()
        self.assertIsNone(budoka)


if __name__ == '__main__':
    unittest.main()
