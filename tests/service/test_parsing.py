import unittest

# project imports
from bushido.utils.dtf import get_datetime_from_timestamp
from bushido.utils import parsing


class TestParsingTimeString(unittest.TestCase):
    def test_parse_manual_datetime_set_correct(self):
        words = ["32", "zarathustra", "--dt", "2024.05.27-1337"]
        timestamp, words = parsing.parse_datetime_to_timestamp(words)
        self.assertEqual(words, ["32", "zarathustra"])
        dt = get_datetime_from_timestamp(timestamp)
        dt_str = dt.strftime("%Y.%m.%d-%H%M")
        self.assertEqual(dt_str, "2024.05.27-1337")

    def test_parse_manual_datetime_set_no_datetime(self):
        words = ["32", "zarathustra", "--dt"]
        with self.assertRaises(ValueError) as context:
            timestamp, words = parsing.parse_datetime_to_timestamp(words)
        self.assertIn("no datetime", str(context.exception))

    def test_parse_manual_datetime_set_no_option(self):
        words = ["32", "zarathustra", "2024.05.27-1337"]
        timestamp, new_words = parsing.parse_datetime_to_timestamp(words)
        self.assertEqual(words, new_words)


if __name__ == "__main__":
    unittest.main()
