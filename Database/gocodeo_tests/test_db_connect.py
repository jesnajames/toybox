import os
import pytest
from unittest import mock
from pymongo import MongoClient
from Database.db_connect import DBConnector

@pytest.fixture
def mock_mongo_client():
    with mock.patch('Database.db_connect.MongoClient') as mock_client:
        yield mock_client

@pytest.fixture
def mock_os_environ():
    with mock.patch.dict(os.environ, {
        "DB_HOST": "localhost",
        "DB_PORT": "27017"
    }):
        yield

@pytest.fixture
def db_connector(mock_mongo_client, mock_os_environ):
    connector = DBConnector()
    yield connector

@pytest.fixture
def mock_database(db_connector):
    mock_db = mock.Mock()
    db_connector.database = mock_db
    yield mock_db

@pytest.fixture
def mock_collection(mock_database):
    mock_collection = mock.Mock()
    mock_database.__getitem__.return_value = mock_collection
    yield mock_collection

@pytest.fixture
def mock_find_one(mock_collection):
    mock_collection.find_one = mock.Mock(return_value={'name': 'test_item', 'value': 'test_value'})
    yield

@pytest.fixture
def mock_insert_one(mock_collection):
    mock_collection.insert_one = mock.Mock(return_value=mock.Mock(inserted_id='ObjectId'))
    yield

@pytest.fixture
def mock_update_one(mock_collection):
    mock_collection.update_one = mock.Mock()
    yield

# happy_path - test_get_database_initializes_client - Test that the database client is initialized when not already set
def test_get_database_initializes_client(db_connector, mock_mongo_client):
    db_connector.get_database()
    mock_mongo_client.assert_called_once_with(host='localhost', port=27017)

# happy_path - test_get_item_returns_correct_document - Test that the correct document is returned from the collection
def test_get_item_returns_correct_document(db_connector, mock_find_one):
    result = db_connector.get_item('test_collection', 'name', 'test_item')
    assert result == {'name': 'test_item', 'value': 'test_value'}

# happy_path - test_add_item_success - Test that a document is successfully added to the collection
def test_add_item_success(db_connector, mock_insert_one):
    result = db_connector.add_item('test_collection', {'name': 'new_item', 'value': 'new_value'})
    assert result.inserted_id == 'ObjectId'

# happy_path - test_update_item_success - Test that a document is successfully updated in the collection
def test_update_item_success(db_connector, mock_update_one, mock_collection):
    db_connector.update_item('test_collection', 'name', 'existing_item', {'value': 'updated_value'})
    mock_collection.update_one.assert_called_once_with({'name': 'existing_item'}, {'$set': {'value': 'updated_value'}})

# happy_path - test_get_database_does_not_reinitialize_client - Test that get_database does not reinitialize db_client if already set
def test_get_database_does_not_reinitialize_client(db_connector, mock_mongo_client):
    db_connector.db_client = 'Existing MongoClient instance'
    db_connector.get_database()
    mock_mongo_client.assert_not_called()

# edge_case - test_get_item_non_existent_document - Test that get_item returns None for a non-existent document
def test_get_item_non_existent_document(db_connector, mock_collection):
    mock_collection.find_one.return_value = None
    result = db_connector.get_item('test_collection', 'name', 'non_existent_item')
    assert result is None

# edge_case - test_add_item_invalid_data - Test that add_item raises an error when adding a document with invalid data
def test_add_item_invalid_data(db_connector, mock_collection):
    with pytest.raises(Exception) as e:
        db_connector.add_item('test_collection', {'name': 123, 'value': 'invalid'})
    assert str(e.value) == 'InvalidDocumentError'

# edge_case - test_update_item_non_existent_document - Test that update_item does not update if the document does not exist
def test_update_item_non_existent_document(db_connector, mock_update_one, mock_collection):
    mock_collection.update_one.return_value.matched_count = 0
    result = db_connector.update_item('test_collection', 'name', 'non_existent_item', {'value': 'new_value'})
    assert result is None

# edge_case - test_get_item_special_characters - Test that get_item handles special characters in key and value
def test_get_item_special_characters(db_connector, mock_collection):
    mock_collection.find_one.return_value = {'name': 'special@item#', 'value': 'special_value'}
    result = db_connector.get_item('test_collection', 'name', 'special@item#')
    assert result == {'name': 'special@item#', 'value': 'special_value'}

# edge_case - test_update_item_nested_fields - Test that update_item handles nested fields in update_dict
def test_update_item_nested_fields(db_connector, mock_update_one, mock_collection):
    db_connector.update_item('test_collection', 'name', 'nested_item', {'details': {'subfield': 'new_sub_value'}})
    mock_collection.update_one.assert_called_once_with({'name': 'nested_item'}, {'$set': {'details': {'subfield': 'new_sub_value'}}})

