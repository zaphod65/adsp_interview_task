from .mongo import MongoDb
import os
import pymongo
import unittest
from unittest.mock import patch

class TestMongoDb(unittest.TestCase):
    @patch('store.database.mongo.pymongo.MongoClient')
    def setUp(self, mongo_mock):
        self.mock_env = {'MONGODB_HOST': 'host', 'MONGODB_DATABASE': 'db'}
        with patch.dict(os.environ, self.mock_env):
            self.db = MongoDb()

    def test_upsert(self):
        test_data = [{'test': 'test'}]

        self.db.database[self.db.collection_name] = unittest.mock.Mock()
        self.db.upsert_many(test_data)

        test_item = test_data[0]
        update = pymongo.UpdateOne(test_item, {'$set': test_item}, upsert=True)
        self.db.database[self.db.collection_name].bulk_write.assert_called_with(
            [update]
        )

    def test_upsert_with_nothing(self):
        test_data = []

        self.db.database[self.db.collection_name] = unittest.mock.Mock()
        self.db.upsert_many(test_data)

        self.db.database[self.db.collection_name].bulk_write.assert_not_called()