import unittest
import peewee as pw

import config
import db
from unit_manager import UnitManager


test_db = pw.SqliteDatabase(':memory:')
models = [db.Agent,
          db.Unit,
          db.Message]


class TestLifting(unittest.TestCase):
    def setUp(self) -> None:
        test_db.bind(models, bind_refs=False, bind_backrefs=False)
        test_db.connect()
        test_db.create_tables(models)
        db.add_agent(agent_id=101, name='N300', is_me=True)
        self.um = UnitManager(config.emojis)

    def tearDown(self) -> None:
        test_db.drop_tables(models)
        test_db.close()


if __name__ == '__main__':
    unittest.main()
