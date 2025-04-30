from pymongo import MongoClient
from bson.objectid import ObjectId

class MongoDB:
    def __init__(self, uri, db_name):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.transactions = self.db["transactions"]

    def insert_transaction(self, transaction_data):
        return self.transactions.insert_one(transaction_data).inserted_id

    def get_all_transactions(self):
        return list(self.transactions.find())

    def get_transaction_by_id(self, transaction_id):
        return self.transactions.find_one({"_id": ObjectId(transaction_id)})
