import unittest
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

# project imports
from bushido.db.db_manager import DatabaseManager
from bushido.db.base_tables import UnitTable, MDEmojiTable
from bushido.db.categories.gym import KeikoTable


class TestBaseDataIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.um = DatabaseManager('sqlite:///:memory:')

    def test_valid_gym_units(self):
        d0 = datetime(2024, 12, 8, 8, 8)
        d1 = datetime(2024, 12, 9, 9, 16)
        emoji = '\U0001F98D'
        t0 = ' '.join([emoji, '0700-0800', 'hm', '//', 'fake training'])
        t1 = ' '.join([emoji, '0830-0930', 'gloria'])
        self.um.process_input(d0.timestamp(), t0)
        self.um.process_input(d1.timestamp(), t1)

        stmt = (select(MDEmojiTable.base_emoji,
                       UnitTable.timestamp,
                       UnitTable.payload,
                       UnitTable.comment,
                       KeikoTable.start_t,
                       KeikoTable.end_t,
                       KeikoTable.gym)
                .join(UnitTable, MDEmojiTable.key == UnitTable.fk_emoji)
                .join(KeikoTable, UnitTable.key == KeikoTable.fk_unit))

        # TODO how to test the date since it's time dependent
        with Session(self.um.engine) as session:
            [r0, r1] = session.execute(stmt).all()
        self.assertEqual(r0[0].encode().decode('unicode_escape'), emoji)
        self.assertEqual(r0[6], 'hm')
        self.assertEqual(r0[2], '0700-0800 hm')
        self.assertEqual(r0[3], 'fake training')

        self.assertEqual(r1[0].encode().decode('unicode_escape'), emoji)
        self.assertEqual(r1[6], 'gloria')
        self.assertEqual(r1[2], '0830-0930 gloria')
        self.assertIsNone(r1[3])


if __name__ == '__main__':
    unittest.main()
