import pymongo

class MongoDb:
    def __init__(self):
        self.collection_name = 'stop_and_search'
        self.database = self.__load_database()
        if self.collection_name not in self.database.list_collection_names():
            self.database.create_collection(self.collection_name)


    def __get_environment(self, name: str) -> str:
        try:
            return os.environ[name]
        except KeyError:
            # log to some centralised logging service
            print(f'{name} environment variable not set')
            exit(255)


    def __load_database(self) -> pymongo.MongoClient:
        client = pymongo.MongoClient(self.__get_environment('MONGODB_HOST'))

        database = client[self.__get_environment('MONGODB_DATABASE')]

        return database


    def __get_upsert(self, item: dict):
        return pymongo.UpdateOne(item, {'$set': item}, upsert=True)


    def upsert_many(self, items: list[dict]):
        if not items:
            return
        collection = self.database['stop_and_search']
        upserts = [self.__get_upsert(item) for item in items]
        collection.bulk_write(upserts)