import unittest
import peewee as pw
import db


test_db = pw.SqliteDatabase(':memory:')
models = [db.Agent,
          db.Unit,
          db.Message]


class TestInitDatabaseIntegration(unittest.TestCase):
    def setUp(self):
        test_db.bind(models)
        test_db.connect()
        test_db.create_tables(models)

    def tearDown(self):
        test_db.drop_tables(models)
        test_db.close()

    def test_init_database(self):
        self.assertTrue(db.Agent.table_exists())
        self.assertTrue(db.Unit.table_exists())
        self.assertTrue(db.Message.table_exists())
        self.assertFalse(test_db.is_closed())

    def test_add_agent(self):
        agent = db.add_agent(0, 'Nietzsche')
        self.assertIsNotNone(agent)

    def test_add_agent_dublicate(self):
        agent0 = db.add_agent(0, 'Kant', False)
        self.assertIsNotNone(agent0)
        agent1 = db.add_agent(0, 'Schopenhauer', False)
        self.assertIsNone(agent1)

    def test_get_me_exists(self):
        db.add_agent(0, 'Platon', True)
        agent = db.get_me()
        self.assertIsNotNone(agent)

    def test_get_me_does_not_exist(self):
        agent0 = db.get_me()
        self.assertIsNone(agent0)


if __name__ == '__main__':
    unittest.main()
