import unittest
import os
from unittest.mock import patch, MagicMock
import peewee as pw

# project imports
from bushido.keikolib.db import init_database, Unit, Message


class TestInitDatabaseMock(unittest.TestCase):
    @patch('bushido.keikolib.db.database')
    @patch('bushido.keikolib.db.logger')
    def test_init_database(self, mock_logger, mock_database):
        # Setup
        data_dir = os.path.join(os.path.expanduser('~'), '.local/share/bushido')
        db_url = os.path.join(data_dir, 'keiko.db')
        mock_db_url = db_url + 'sqlite:///:memory:'
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
        mock_database.create_tables.assert_any_call(models=[Unit, Message], safe=True)
        mock_database.create_tables.assert_any_call(models=mock_models, safe=True)
        mock_database.close.assert_called_once()
        mock_logger.error.assert_not_called()

    @patch('bushido.keikolib.db.database')
    @patch('bushido.keikolib.db.logger')
    def test_init_database_operational_error(self, mock_logger, mock_database):
        # Setup

        data_dir = os.path.join(os.path.expanduser('~'), '.local/share/bushido')
        db_url = os.path.join(data_dir, 'keiko.db')
        mock_db_url = db_url + 'sqlite:///:memory:'
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
