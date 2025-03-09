import unittest

# project imports
from unitlib import UnitManager


class TestPreprocess(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.um = UnitManager('sqlite:///:memory:')

    def test_empty_input_string(self):
        input_string = ''
        with self.assertRaises(ValueError):
            self.um._preprocess_string(input_string)

    def test_comment_symbol_only(self):
        input_string = '//'
        with self.assertRaises(ValueError):
            self.um._preprocess_string(input_string)

    def test_empty_payload(self):
        input_string = '// this is a comment'
        with self.assertRaises(ValueError):
            self.um._preprocess_string(input_string)

    def test_correct_input_without_emoji_no_comment(self):
        input_string = '<emoji> some 101 char 5'
        emoji, words, comment = self.um._preprocess_string(input_string)
        self.assertEqual(emoji, '<emoji>')
        self.assertEqual(words, ['some', '101', 'char', '5'])
        self.assertIsNone(comment)

    def test_correct_input_without_emoji_no_comment_but_symbol(self):
        input_string = '<emoji> 101 5 //'
        emoji, words, comment = self.um._preprocess_string(input_string)
        self.assertEqual(emoji, '<emoji>')
        self.assertEqual(words, ['101', '5'])
        self.assertIsNone(comment)

    def test_correct_input_without_emoji_full(self):
        input_string = '<emoji> some numbers eg 5 // this is a comment'
        emoji, words, comment = self.um._preprocess_string(input_string)
        self.assertEqual(emoji, '<emoji>')
        self.assertEqual(words, ['some', 'numbers', 'eg', '5'])
        self.assertEqual(comment, 'this is a comment')

    def test_correct_input_without_emoji_no_payload(self):
        input_string = '<emoji> // this is a comment'
        emoji, words, comment = self.um._preprocess_string(input_string)
        self.assertEqual(emoji, '<emoji>')
        self.assertEqual(words, [])
        self.assertEqual(comment, 'this is a comment')

    def test_correct_input_without_emoji_no_payload_no_comment(self):
        input_string = '<emoji>'
        emoji, words, comment = self.um._preprocess_string(input_string)
        self.assertEqual(emoji, '<emoji>')
        self.assertEqual(words, [])
        self.assertIsNone(comment)


if __name__ == '__main__':
    unittest.main()
