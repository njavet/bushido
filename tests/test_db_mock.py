import unittest
from unittest.mock import patch, MagicMock
import peewee as pw

# project imports
from bushido.db import init_database, Budoka, Unit, Message


class TestInitDatabaseMock(unittest.TestCase):
    @patch('bushido.db.database')
    @patch('bushido.db.logger')
    def test_init_database(self, mock_logger, mock_database):
        # Setup
        mock_db_url = 'sqlite:///:memory:'
        mock_models = [MagicMock(), MagicMock()]

        # Mock methods
        mock_database.connect = MagicMock()
        mock_database.create_tables = MagicMock()
        mock_database.close = MagicMock()

        # Execute
        init_database(mock_db_url, mock_models)

        # Assertions
        mock_database.init.assert_called_once_with(mock_db_url)
        mock_database.connect.assert_called_once()
        mock_database.create_tables.assert_any_call(models=[Budoka, Unit, Message], safe=True)
        mock_database.create_tables.assert_any_call(models=mock_models, safe=True)
        mock_database.close.assert_called_once()
        mock_logger.error.assert_not_called()

    @patch('bushido.db.database')
    @patch('bushido.db.logger')
    def test_init_database_operational_error(self, mock_logger, mock_database):
        # Setup
        mock_db_url = 'sqlite:///:memory:'
        mock_models = [MagicMock(), MagicMock(), MagicMock()]

        # Mock methods
        mock_database.connect.side_effect = pw.OperationalError('Connection failed')

        # Execute
        with self.assertRaises(SystemExit):
            init_database(mock_db_url, mock_models)

        # Assertions
        mock_database.init.assert_called_once_with(mock_db_url)
        mock_database.connect.assert_called_once()
        mock_logger.error.assert_called_once_with('peewee operational error: Connection failed')


if __name__ == '__main__':
    unittest.main()
