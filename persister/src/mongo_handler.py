from pymongo import MongoClient


class MongoHandler:
    def __init__(self, uri: str, db_name: str):
        # Fast fail if Mongo is unreachable
        self.client = MongoClient(uri, serverSelectionTimeoutMS=3000)
        try:
            self.client.admin.command("ping")
        except Exception:
            # Let caller decide how to handle; writes will still retry internally
            pass
        self.db = self.client[db_name]

    def insert_one(self, collection: str, document: dict) -> None:
        self.db[collection].insert_one(document)

    def close(self) -> None:
        self.client.close()