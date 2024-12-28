import unittest
import datetime

# project imports
from ulib.utils import parsing


class TestParsingTimeString(unittest.TestCase):
    def test_parse_time_string_HH_MM_SS_0(self):
        ts = '02:24:59'
        sec = parsing.parse_time_string(ts)
        self.assertEqual(8699.0, sec)

    def test_parse_time_string_HH_MM_SS_1(self):
        ts = '1:02:03'
        sec = parsing.parse_time_string(ts)
        self.assertEqual(3723.0, sec)

    def test_parse_time_string_HH_MM_SS_2(self):
        ts = '2:4:1'
        sec = parsing.parse_time_string(ts)
        self.assertEqual(7441.0, sec)

    def test_parse_time_string_MM_SS_0(self):
        ts = '32:29'
        sec = parsing.parse_time_string(ts)
        self.assertEqual(1949.0, sec)

    def test_parse_time_string_MM_SS_2(self):
        ts = '1:20'
        sec = parsing.parse_time_string(ts)
        self.assertEqual(80.0, sec)

    def test_parse_time_string_minutes(self):
        ts = '16'
        sec = parsing.parse_time_string(ts)
        self.assertEqual(960.0, sec)

    def test_parse_time_string_hours(self):
        ts = '2h'
        sec = parsing.parse_time_string(ts)
        self.assertEqual(7200.0, sec)

    def test_parse_time_string_seconds(self):
        ts = '32s'
        sec = parsing.parse_time_string(ts)
        self.assertEqual(32.0, sec)

    def test_parse_time_string_wrong_input_0(self):
        ts = 'not a valid time_string'
        sec = parsing.parse_time_string(ts)
        self.assertRaises(ValueError)

    def test_parse_time_string_wrong_input_1(self):
        ts = '32five'
        sec = parsing.parse_time_string(ts)
        self.assertRaises(ValueError)


class TestParsingMilitaryTimeString(unittest.TestCase):
    def test_parse_military_time_string_0(self):
        ts = '1600'
        mt = parsing.parse_military_time_string(ts)
        self.assertEqual(datetime.time(16, 0), mt)


if __name__ == '__main__':
    unittest.main()
