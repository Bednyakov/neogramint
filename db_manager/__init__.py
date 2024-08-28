from pymongo import MongoClient


class DBManager:
    def __init__(self, db_name: str) -> None:
        self.client = MongoClient("mongodb://localhost:27017/")
        self.db = self.client[db_name]

    def create_collection(self, name: str):
        collection = self.db[name]
        return collection

