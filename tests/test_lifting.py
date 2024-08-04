import unittest
import peewee as pw

# project imports
from bushido.keikolib.db import Unit, Message
from bushido.keikolib import UnitManager


test_db = pw.SqliteDatabase(':memory:')
models = [Unit, Message]


class TestLifting(unittest.TestCase):
    def setUp(self) -> None:
        test_db.bind(models, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(models)
        self.um = UnitManager()

    def tearDown(self) -> None:
        test_db.drop_tables(models)
        test_db.close()


if __name__ == '__main__':
    unittest.main()
