from pymongo import MongoClient
import os
from dotenv import load_dotenv
load_dotenv()

class DBConnector():
    def __init__(self):
        self.db_client = None

    def get_database(self):
        if self.db_client is None:
            self.db_client = MongoClient(host=os.environ["DB_HOST"], port=int(os.environ["DB_PORT"]))
        self.database = self.db_client["toybox"]

    def get_item(self, collection_name, key, value):
        self.get_database()
        collection = self.database[collection_name]
        doc = collection.find_one({key: value})
        return doc
    
    def add_item(self, collection_name, document):
        self.get_database()
        collection = self.database[collection_name]
        item = collection.insert_one(document)
        return item
    
    def update_item(self, collection_name, key, value, update_dict):
        print(f"Updating document with {key}:{value} as {update_dict}")
        self.get_database()
        collection = self.database[collection_name]
        collection.update_one({key:value}, { "$set": update_dict })
        return update_dict
