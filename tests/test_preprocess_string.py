import unittest
from typing import Optional

# project impots
from bushido.keikolib.filters import preprocess_string


class TestPreprocessString(unittest.TestCase):

    def test_preprocess_string_valid_input_with_comment(self):
        input_string = "😀 hello world // this is a comment"
        expected_output = ("😀", ["hello", "world"], "this is a comment")
        result = preprocess_string(input_string)
        self.assertEqual(result, expected_output)

    def test_preprocess_string_valid_input_without_comment(self):
        input_string = "😀 hello world"
        expected_output = ("😀", ["hello", "world"], None)
        result = preprocess_string(input_string)
        self.assertEqual(result, expected_output)

    def test_preprocess_string_empty_payload(self):
        input_string = "// this is a comment"
        with self.assertRaises(ValueError):
            preprocess_string(input_string)

    def test_preprocess_string_only_emoji(self):
        input_string = "😀 // this is a comment"
        expected_output = ("😀", [], "this is a comment")
        result = preprocess_string(input_string)
        self.assertEqual(result, expected_output)

    def test_preprocess_string_only_emoji_no_comment(self):
        input_string = "😀"
        expected_output = ("😀", [], None)
        result = preprocess_string(input_string)
        self.assertEqual(result, expected_output)

    def test_preprocess_string_no_emoji_payload(self):
        input_string = "//"
        with self.assertRaises(ValueError):
            preprocess_string(input_string)

    def test_preprocess_string_empty_string(self):
        input_string = ""
        with self.assertRaises(ValueError):
            preprocess_string(input_string)


if __name__ == '__main__':
    unittest.main()
