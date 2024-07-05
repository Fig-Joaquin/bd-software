# tests/test_mongodb_manager.py
import pytest
from database_manager.mongodb_manager import MongoDBManager

@pytest.fixture
def mongodb_manager():
    return MongoDBManager()

def test_show_collections(mongodb_manager):
    collections = mongodb_manager.show_collections()
    assert isinstance(collections, list)

def test_insert_document(mongodb_manager):
    document = {"name": "test"}
    result = mongodb_manager.insert_document("test_collection", document)
    assert result.inserted_id is not None

def test_find_documents(mongodb_manager):
    query = {"name": "test"}
    documents = mongodb_manager.find_documents("test_collection", query)
    assert isinstance(documents, list)
