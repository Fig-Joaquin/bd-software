from pymongo import MongoClient
from .config import Config
import json

class MongoDBManager:
    def __init__(self, uri=Config.MONGODB_URI, dbname=Config.MONGODB_DBNAME):
        self.client = MongoClient(uri)
        self.db = self.client[dbname]
    
    def show_collections(self):
        return self.db.list_collection_names()
    
    def insert_document(self, collection_name, document):
        collection = self.db[collection_name]
        return collection.insert_one(document)
    
    def insert_documents(self, collection_name, documents):
        collection = self.db[collection_name]
        return collection.insert_many(documents)
    
    def find_documents(self, collection_name, query):
        collection = self.db[collection_name]
        return list(collection.find(query))
    
    def find_documents_with_aggregate(self, collection_name, pipeline):
        collection = self.db[collection_name]
        return list(collection.aggregate(pipeline))
    
    def load_data_from_json(self, collection_name, file_path):
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        self.insert_documents(collection_name, data)
