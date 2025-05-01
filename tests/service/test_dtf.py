import datetime
import unittest

# project imports
from bushido.utils import dtf

class TestDTF(unittest.TestCase):
    def test_find_previous_sunday(self):
        today = datetime.date(2025, 5, 1)
        prev_sunday = dtf.find_previous_sunday(today)
        self.assertEqual(prev_sunday, datetime.date(2025, 4, 27))


if __name__ == '__main__':
    unittest.main()
