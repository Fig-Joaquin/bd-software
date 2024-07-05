from pymongo import MongoClient
from config import Config

def main():
    client = MongoClient(Config.MONGODB_URI)
    db = client[Config.MONGODB_DBNAME]
    collection = db['data_eng_salaries']

    # Verifica los primeros 5 documentos en la colección
    documents = collection.find().limit(5)
    for doc in documents:
        print(doc)

if __name__ == "__main__":
    main()
