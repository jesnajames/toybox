import os
import pytest
from unittest.mock import patch, MagicMock
from pymongo import MongoClient
from dotenv import load_dotenv

# Mocking load_dotenv to avoid loading actual environment variables
load_dotenv = MagicMock()

# Mocking MongoClient
mocked_mongo_client = MagicMock(spec=MongoClient)
mocked_database = MagicMock()
mocked_collection = MagicMock()

@pytest.fixture
def db_connector():
    with patch('Database.db_connect.MongoClient', return_value=mocked_mongo_client):
        from Database.db_connect import DBConnector
        connector = DBConnector()
        mocked_mongo_client.__getitem__.return_value = mocked_database
        mocked_database.__getitem__.return_value = mocked_collection
        yield connector

@pytest.fixture
def mock_env_vars():
    with patch.dict(os.environ, {"DB_HOST": "localhost", "DB_PORT": "27017"}):
        yield

# Mocking MongoClient methods
mocked_collection.find_one.return_value = {"name": "toy", "price": 10}
mocked_collection.insert_one.return_value.inserted_id = "mocked_id"
mocked_collection.update_one.return_value = None

# happy_path - get_item - Test that get_item retrieves a document with the specified key-value pair from the collection.
def test_get_item_existing_document(db_connector, mock_env_vars):
    result = db_connector.get_item(collection_name='test_collection', key='name', value='toy')
    assert result == {'name': 'toy', 'price': 10}

# happy_path - add_item - Test that add_item inserts a new document into the specified collection and returns the inserted ID.
def test_add_item(db_connector, mock_env_vars):
    result = db_connector.add_item(collection_name='test_collection', document={'name': 'new_toy', 'price': 15})
    assert result.inserted_id == 'mocked_id'

# happy_path - update_item - Test that update_item updates the document with the specified key-value pair using the update dictionary.
def test_update_item(db_connector, mock_env_vars):
    with patch.object(mocked_collection, 'update_one', return_value=None) as mock_update:
        result = db_connector.update_item(collection_name='test_collection', key='name', value='toy', update_dict={'price': 20})
        mock_update.assert_called_once_with({'name': 'toy'}, {'$set': {'price': 20}})
    assert result == {'price': 20}

# happy_path - get_database - Test that get_database initializes the database client if it is not already initialized.
def test_get_database_initialization(db_connector, mock_env_vars):
    db_connector.get_database()
    assert db_connector.db_client is not None

# happy_path - add_item - Test that add_item can handle inserting documents with nested structures.
def test_add_item_with_nested_document(db_connector, mock_env_vars):
    result = db_connector.add_item(collection_name='test_collection', document={'name': 'nested_toy', 'details': {'color': 'red', 'size': 'medium'}})
    assert result.inserted_id == 'mocked_id'

# edge_case - get_item - Test that get_item returns None when no document matches the specified key-value pair.
def test_get_item_nonexistent_document(db_connector, mock_env_vars):
    mocked_collection.find_one.return_value = None
    result = db_connector.get_item(collection_name='test_collection', key='name', value='nonexistent')
    assert result is None

# edge_case - add_item - Test that add_item raises an error when inserting a document with an invalid structure.
def test_add_item_invalid_document(db_connector, mock_env_vars):
    with pytest.raises(TypeError):
        db_connector.add_item(collection_name='test_collection', document=None)

# edge_case - update_item - Test that update_item does nothing when no document matches the specified key-value pair.
def test_update_item_nonexistent_document(db_connector, mock_env_vars):
    with patch.object(mocked_collection, 'update_one', return_value=None) as mock_update:
        result = db_connector.update_item(collection_name='test_collection', key='name', value='nonexistent', update_dict={'price': 25})
        mock_update.assert_called_once_with({'name': 'nonexistent'}, {'$set': {'price': 25}})
    assert result == {'price': 25}

# edge_case - get_database - Test that get_database raises an error if the environment variables are not set.
def test_get_database_missing_env_vars(db_connector):
    with patch.dict(os.environ, {}, clear=True):
        with pytest.raises(KeyError):
            db_connector.get_database()

# edge_case - update_item - Test that update_item can handle updating documents with empty update dictionaries.
def test_update_item_empty_update_dict(db_connector, mock_env_vars):
    with patch.object(mocked_collection, 'update_one', return_value=None) as mock_update:
        result = db_connector.update_item(collection_name='test_collection', key='name', value='toy', update_dict={})
        mock_update.assert_called_once_with({'name': 'toy'}, {'$set': {}})
    assert result == {}

