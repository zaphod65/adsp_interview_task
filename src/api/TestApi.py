from .api import ApiClient
import json
import requests
import unittest
from unittest.mock import patch, Mock
from urllib3.exceptions import HTTPError

class TestApi(unittest.TestCase):
    @patch('requests.get')
    def test_successful_request(self, test_get):
        response_data = [{'test': 'test'}]
        force = 'greater_manchester'
        date = '2024-01'

        mock_response = Mock()
        mock_response.text = json.dumps(response_data)

        test_get.return_value = mock_response

        result = ApiClient.request_searches(force, date)
        test_get.assert_called_with(
            'https://data.police.uk/api/stops-force',
            params={
                'date': date,
                'force': force,
            },
            headers={
                'accept': 'application/json',
            }
        )

        self.assertEqual(result, response_data)

    @patch('requests.get')
    def test_failed_request(self, test_get):
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = HTTPError()
        test_get.return_value = mock_response

        with self.assertRaises(HTTPError):
            result = ApiClient.request_searches('force', 'date')
