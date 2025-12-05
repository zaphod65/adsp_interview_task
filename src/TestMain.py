from datetime import date
from dateutil.relativedelta import relativedelta
from main import main
import os
import unittest
from unittest.mock import patch, Mock


class TestMain(unittest.TestCase):
    def test_main_calls_correct_methods(self):
        args = {}
        mock_env = {
            'FORCES': 'place'
        }
        mock_store = Mock()
        mock_api = Mock()
        mock_api.request_searches.return_value = []
        with patch.dict(os.environ, mock_env):
            main(args, mock_store, mock_api)

        two_months_ago = date.today() + relativedelta(months=-2)
        search_date = two_months_ago.strftime('%Y-%m')

        mock_api.request_searches.assert_called_once_with('place', search_date)
        mock_store.mass_upsert.assert_called_once_with([])

    def test_main_calls_methods_once_per_force(self):
        args = {}
        mock_env = {
            'FORCES': 'test,place'
        }
        mock_store = Mock()
        mock_api = Mock()
        mock_api.request_searches.return_value = []
        with patch.dict(os.environ, mock_env):
            main(args, mock_store, mock_api)

        two_months_ago = date.today() + relativedelta(months=-2)
        search_date = two_months_ago.strftime('%Y-%m')

        self.assertEqual(2, mock_api.request_searches.call_count)
        self.assertEqual(2, mock_store.mass_upsert.call_count)

    def test_main_respects_script_args(self):
        force = 'somewhere'
        args_date = '1987-03'
        args = {
            'force': force,
            'no_store': True,
            'date': args_date
        }
        mock_env = {
            'FORCES': 'different',
        }

        mock_store = Mock()
        mock_api = Mock()
        mock_api.request_searches.return_value = []
        with patch.dict(os.environ, mock_env):
            with self.assertRaises(SystemExit):
                main(args, mock_store, mock_api)

        mock_store.mass_upsert.assert_not_called()
        mock_api.request_searches.assert_called_once_with(force, args_date)