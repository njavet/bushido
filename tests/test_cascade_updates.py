import unittest


# project imports
from ulib.db import DatabaseManager


class TestCategoryEmojiCascade(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        dbm = DatabaseManager('sqlite:///:memory:')
