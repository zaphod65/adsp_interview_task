from store import Store
import unittest
from unittest.mock import patch

class TestStore(unittest.TestCase):
    def setUp(self):
        self.mock_database = unittest.mock.Mock()
        self.store = Store(self.mock_database)

    def test_upsert(self):
        test_data = [{'test': 'test'}]
        self.store.mass_upsert(test_data)

        self.mock_database.upsert_many.assert_called_with(test_data)