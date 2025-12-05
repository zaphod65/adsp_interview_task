from .database.mongo import MongoDb


class Store:
    def __init__(self, db = None):
        if db is None:
            self.database = MongoDb()
        else:
            self.database = db


    def mass_upsert(self, items: list[dict]):
        self.database.upsert_many(items)
