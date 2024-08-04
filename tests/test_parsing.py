import unittest

# project imports
import bushido.keikolib.parsing as parsing


class TestParsingTimeString(unittest.TestCase):
    def test_parse_manual_datetime_set_correct(self):
        words = ['32', 'zarathustra', '-dt', '270524-1337']
        option = '-dt'
        value = parsing.parse_option(words, option)
        self.assertEqual(value, '270524-1337')

    def test_parse_manual_datetime_set_no_datetime(self):
        words = ['32', 'zarathustra', '-dt']
        option = '-dt'
        res = parsing.parse_option(words, option)
        self.assertEqual(res, None)

    def test_parse_manual_datetime_set_no_option(self):
        words = ['32', 'zarathustra', '270524-1337']
        option = '-dt'
        res = parsing.parse_option(words, option)
        self.assertEqual(res, None)


if __name__ == '__main__':
    unittest.main()
