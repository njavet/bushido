import unittest
from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime

# project imports
from bushido.data.manager import DataManager
from bushido.data.db_init import db_init
from bushido.data.base_tables import UnitTable, MDEmojiTable
from bushido.data.categories.gym import KeikoTable
from bushido.service.units import UnitProcessor
from bushido.web.units import create_unit_spec


class TestBaseDataIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dm = DataManager('sqlite:///:memory:')
        db_init(dm.engine)
        cls.up = UnitProcessor(dm)

    def test_valid_gym_units(self):
        unit_name = 'weights'
        words0 = ['0700-0800', 'hm']
        words1 = ['0830-0930', 'gloria']
        unit_spec0 = create_unit_spec(unit_name, words0, 'fake training')
        unit_spec1 = create_unit_spec(unit_name, words1, comment=None)
        self.up.process_input(unit_spec0)
        self.up.process_input(unit_spec1)

        stmt = (select(MDEmojiTable.unit_name,
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
        self.assertEqual(r0[0], unit_name)
        self.assertEqual(r0[6], 'hm')
        self.assertEqual(r0[2], '0700-0800 hm')
        self.assertEqual(r0[3], 'fake training')

        self.assertEqual(r1[0], unit_name)
        self.assertEqual(r1[6], 'gloria')
        self.assertEqual(r1[2], '0830-0930 gloria')
        self.assertIsNone(r1[3])


if __name__ == '__main__':
    unittest.main()
