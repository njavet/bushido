import unittest
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

# project imports
from bushido.db import DatabaseManager
from bushido.services.unit_manager import UnitManager
from bushido.db.models import Unit, Gym


class TestBaseDataIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dbm = DatabaseManager('sqlite:///:memory:')
        dbm.init_tables()
        dbm.upload_category_data()
        dbm.upload_emoji_data()
        cls.um = UnitManager(dbm)

    def test_valid_gym_units(self):
        d0 = datetime(2024, 12, 8, 8, 8)
        d1 = datetime(2024, 12, 9, 9, 16)
        d2 = datetime(2024, 12, 10, 10, 32)
        emoji = '\U0001F98D'.encode().decode('unicode_escape')
        t0 = ' '.join([emoji, '0700-0800', 'hm', '//', 'fake training'])
        t1 = ' '.join([emoji, '0800-0900', 'hm', '//', 'again a fake training'])
        t2 = ' '.join([emoji, '0830-0930', 'gloria'])
        self.um.process_input(d0.timestamp(), t0)
        self.um.process_input(d1.timestamp(), t1)
        self.um.process_input(d2.timestamp(), t2)

        with Session(self.um.dbm.engine) as session:
            stmt = select(Unit, Gym).join(Gym)
            res = session.execute(stmt).all()

        print(res)
if __name__ == '__main__':
    unittest.main()
