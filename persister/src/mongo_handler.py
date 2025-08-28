from pymongo import MongoClient


class MongoHandler:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_one(self, collection: str, document: dict) -> None:
        self.db[collection].insert_one(document)

    def close(self) -> None:
        self.client.close()