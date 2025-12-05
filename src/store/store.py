from .database import MongoDb


class Store:
    def __init__(self):
        self.database = MongoDb()


    def mass_upsert(self, items: list[dict]):
        self.database.upsert_many(items)
