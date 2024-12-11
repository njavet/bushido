import unittest
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

# project imports
from ulib.db import DatabaseManager
from ulib.services.unit_manager import UnitManager
from ulib.db.models import Unit, Gym, Emoji, Message


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
        emoji = '\U0001F98D'
        t0 = ' '.join([emoji, '0700-0800', 'hm', '//', 'fake training'])
        t1 = ' '.join([emoji, '0830-0930', 'gloria'])
        self.um.process_input(d0.timestamp(), t0)
        self.um.process_input(d1.timestamp(), t1)

        stmt = (select(Emoji.emoji_base,
                       Unit.unix_timestamp,
                       Gym.start_t,
                       Gym.end_t,
                       Gym.gym,
                       Message.payload,
                       Message.comment)
                .join(Unit, Emoji.key == Unit.emoji)
                .join(Gym, Unit.key == Gym.key)
                .join(Message, Message.key == Unit.key))

        # TODO how to test the date since it's time dependent
        with Session(self.um.dbm.engine) as session:
            [r0, r1] = session.execute(stmt).all()
        self.assertEqual(r0[0].encode().decode('unicode_escape'), emoji)
        self.assertEqual(r0[4], 'hm')
        self.assertEqual(r0[5], '0700-0800 hm')
        self.assertEqual(r0[6], 'fake training')

        self.assertEqual(r1[0].encode().decode('unicode_escape'), emoji)
        self.assertEqual(r1[4], 'gloria')
        self.assertEqual(r1[5], '0830-0930 gloria')
        self.assertIsNone(r1[6])


if __name__ == '__main__':
    unittest.main()
