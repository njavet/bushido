import unittest

# project imports
from bushido.utils.parsing import preprocess_input


class TestPreprocess(unittest.TestCase):
    def test_empty_input_string(self):
        input_string = ""
        with self.assertRaises(ValueError):
            preprocess_input(input_string)

    def test_comment_symbol_only(self):
        input_string = "#"
        with self.assertRaises(ValueError):
            preprocess_input(input_string)

    def test_empty_payload(self):
        input_string = "# this is a comment"
        with self.assertRaises(ValueError):
            preprocess_input(input_string)

    def test_correct_input_without_emoji_no_comment(self):
        input_string = "<emoji> some 101 char 5"
        unit_name, words, comment = preprocess_input(input_string)
        self.assertEqual(unit_name, "<emoji>")
        self.assertEqual(words, ["some", "101", "char", "5"])
        self.assertIsNone(comment)

    def test_correct_input_without_emoji_no_comment_but_symbol(self):
        input_string = "<emoji> 101 5 #"
        unit_name, words, comment = preprocess_input(input_string)
        self.assertEqual(unit_name, "<emoji>")
        self.assertEqual(words, ["101", "5"])
        self.assertIsNone(comment)

    def test_correct_input_without_emoji_full(self):
        input_string = "<emoji> some numbers eg 5 # this is a comment"
        unit_name, words, comment = preprocess_input(input_string)
        self.assertEqual(unit_name, "<emoji>")
        self.assertEqual(words, ["some", "numbers", "eg", "5"])
        self.assertEqual(comment, "this is a comment")

    def test_correct_input_without_emoji_no_payload(self):
        input_string = "<emoji> # this is a comment"
        unit_name, words, comment = preprocess_input(input_string)
        self.assertEqual(unit_name, "<emoji>")
        self.assertEqual(words, [])
        self.assertEqual(comment, "this is a comment")

    def test_correct_input_without_emoji_no_payload_no_comment(self):
        input_string = "<emoji>"
        unit_name, words, comment = preprocess_input(input_string)
        self.assertEqual(unit_name, "<emoji>")
        self.assertEqual(words, [])
        self.assertIsNone(comment)


if __name__ == "__main__":
    unittest.main()
