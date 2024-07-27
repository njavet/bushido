import unittest
import peewee as pw

# project imports
from bushido.db import Budoka, Unit, Message, add_budoka
from bushido.manager import UnitManager


test_db = pw.SqliteDatabase(':memory:')
models = [Budoka,
          Unit,
          Message]


class TestLifting(unittest.TestCase):
    def setUp(self) -> None:
        test_db.bind(models, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(models)
        add_budoka(budoka_id=101, name='N300', is_me=True)
        self.um = UnitManager()

    def tearDown(self) -> None:
        test_db.drop_tables(models)
        test_db.close()


if __name__ == '__main__':
    unittest.main()
