import unittest
from unittest.mock import patch, MagicMock
import peewee as pw

# project imports
from bushido.db import add_budoka, get_me, Budoka


class TestDatabaseFunctions(unittest.TestCase):

    @patch('bushido.db.Budoka')
    def test_add_budoka_success(self, mock_budoka):
        mock_budoka.create.return_value = MagicMock(spec=Budoka)
        budoka_id = 1
        name = "John Doe"
        is_me = False

        result = add_budoka(budoka_id, name, is_me)

        mock_budoka.create.assert_called_once_with(budoka_id=budoka_id, name=name, is_me=is_me)
        self.assertIsInstance(result, Budoka)

    @patch('bushido.db.Budoka')
    def test_add_budoka_integrity_error(self, mock_budoka):
        mock_budoka.create.side_effect = pw.IntegrityError
        budoka_id = 1
        name = "John Doe"
        is_me = False

        result = add_budoka(budoka_id, name, is_me)

        mock_budoka.create.assert_called_once_with(budoka_id=budoka_id, name=name, is_me=is_me)
        self.assertIsNone(result)

    @patch('bushido.db.logger')
    @patch('bushido.db.Budoka')
    def test_get_me_success(self, mock_budoka, mock_logger):
        mock_budoka.get.return_value = MagicMock(spec=Budoka)

        result = get_me()

        mock_budoka.get.assert_called_once_with(is_me=True)
        self.assertIsInstance(result, Budoka)
        mock_logger.debug.assert_not_called()

    @patch('bushido.db.logger')
    @patch('bushido.db.Budoka')
    def test_get_me_does_not_exist(self, mock_budoka, mock_logger):
        mock_budoka.get.side_effect = pw.DoesNotExist

        result = get_me()

        mock_budoka.get.assert_called_once_with(is_me=True)
        self.assertIsNone(result)
        mock_logger.debug.assert_called_once_with('Budoka does not exist...')

    @patch('bushido.db.logger')
    @patch('bushido.db.Budoka')
    def test_get_me_operational_error(self, mock_budoka, mock_logger):
        mock_budoka.get.side_effect = pw.OperationalError

        result = get_me()

        mock_budoka.get.assert_called_once_with(is_me=True)
        self.assertIsNone(result)
        mock_logger.debug.assert_called_once_with('operational error... ')


if __name__ == '__main__':
    unittest.main()
