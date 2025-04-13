import unittest
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

# project imports
from bushido.data.manager import DataManager
from bushido.data.db_init import db_init
from bushido.data.base_tables import UnitTable, MDEmojiTable
from bushido.data.categories.gym import KeikoTable, create_keiko_orm
from bushido.service.units import UnitProcessor
from bushido.service.categories.gym import parse_unit


class TestBaseDataIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dm = DataManager('sqlite:///:memory:')
        db_init(dm.engine)
        cls.up = UnitProcessor(dm)

    def test_valid_gym_units(self):
        emoji = '\U0001F98D'.encode().decode()
        t0 = ' '.join([emoji, '0700-0800', 'hm', '//', 'fake training'])
        t1 = ' '.join([emoji, '0830-0930', 'gloria'])
        self.up.process_input(t0, parse_unit, create_keiko_orm)
        self.up.process_input(t1, parse_unit, create_keiko_orm)

        stmt = (select(MDEmojiTable.emoji,
                       UnitTable.timestamp,
                       UnitTable.payload,
                       UnitTable.comment,
                       KeikoTable.start_t,
                       KeikoTable.end_t,
                       KeikoTable.gym)
                .join(UnitTable, MDEmojiTable.key == UnitTable.fk_emoji)
                .join(KeikoTable, UnitTable.key == KeikoTable.fk_unit))

        # TODO how to test the date since it's time dependent
        with Session(self.up.dm.engine) as session:
            [r0, r1] = session.execute(stmt).all()
        self.assertEqual(r0[0], emoji)
        self.assertEqual(r0[6], 'hm')
        self.assertEqual(r0[2], '0700-0800 hm')
        self.assertEqual(r0[3], 'fake training')

        self.assertEqual(r1[0], emoji)
        self.assertEqual(r1[6], 'gloria')
        self.assertEqual(r1[2], '0830-0930 gloria')
        self.assertIsNone(r1[3])


if __name__ == '__main__':
    unittest.main()
