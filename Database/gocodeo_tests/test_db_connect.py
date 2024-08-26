import pytest
from unittest.mock import patch, MagicMock
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient
import os

@pytest.fixture
def mock_env_vars():
    with patch.dict(os.environ, {"DB_HOST": "mockhost", "DB_PORT": "27017"}):
        yield

@pytest.fixture
def mock_mongo_client():
    with patch('pymongo.MongoClient') as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        yield mock_instance

@pytest.fixture
def db_connector(mock_env_vars, mock_mongo_client):
    from your_module import DBConnector  # Replace 'your_module' with the actual module name
    return DBConnector()

@pytest.fixture
def mock_collection():
    mock_collection = MagicMock()
    yield mock_collection

@pytest.fixture
def mock_database(mock_mongo_client, mock_collection):
    mock_database = MagicMock()
    mock_database.__getitem__.return_value = mock_collection
    mock_mongo_client.__getitem__.return_value = mock_database
    yield mock_database

@pytest.fixture
def mock_insert_one(mock_collection):
    mock_insert_result = MagicMock()
    mock_insert_result.inserted_id = "mocked_object_id"
    mock_collection.insert_one.return_value = mock_insert_result
    yield mock_insert_result

@pytest.fixture
def mock_find_one(mock_collection):
    mock_find_result = MagicMock()
    mock_collection.find_one.return_value = mock_find_result
    yield mock_find_result

@pytest.fixture
def mock_update_one(mock_collection):
    mock_update_result = MagicMock()
    mock_collection.update_one.return_value = mock_update_result
    yield mock_update_result

@pytest.fixture
def mock_connection_failure():
    with patch('pymongo.MongoClient', side_effect=ConnectionFailure):
        yield

# happy_path - get_database - Test that the database client is initialized when calling get_database method for the first time.
def test_get_database_initialization(db_connector, mock_mongo_client):
    db_connector.get_database()
    assert db_connector.db_client == mock_mongo_client
    assert db_connector.database == mock_mongo_client['toybox']

# happy_path - get_item - Test that an item is retrieved from the collection based on key-value pair.
def test_get_item_retrieval(db_connector, mock_find_one, mock_collection):
    mock_find_one.return_value = {'name': 'test_item'}
    result = db_connector.get_item('test_collection', 'name', 'test_item')
    mock_collection.find_one.assert_called_once_with({'name': 'test_item'})
    assert result == {'name': 'test_item'}

# happy_path - add_item - Test that a document is added to the specified collection.
def test_add_item_to_collection(db_connector, mock_insert_one, mock_collection):
    document = {'name': 'new_item'}
    result = db_connector.add_item('test_collection', document)
    mock_collection.insert_one.assert_called_once_with(document)
    assert result.inserted_id == "mocked_object_id"

# happy_path - update_item - Test that an existing document is updated with new values.
def test_update_item_in_collection(db_connector, mock_update_one, mock_collection):
    update_dict = {'name': 'updated_item'}
    result = db_connector.update_item('test_collection', 'name', 'existing_item', update_dict)
    mock_collection.update_one.assert_called_once_with({'name': 'existing_item'}, {'$set': update_dict})
    assert result == update_dict

# happy_path - get_database - Test that the database is connected on multiple operations without reinitialization.
def test_database_connection_persistence(db_connector, mock_mongo_client):
    db_connector.get_database()
    first_client = db_connector.db_client
    db_connector.get_database()
    assert db_connector.db_client == first_client
    assert mock_mongo_client.call_count == 1

# edge_case - get_item - Test that get_item returns None when the key-value pair does not exist.
def test_get_item_non_existent(db_connector, mock_find_one, mock_collection):
    mock_find_one.return_value = None
    result = db_connector.get_item('test_collection', 'name', 'non_existent_item')
    mock_collection.find_one.assert_called_once_with({'name': 'non_existent_item'})
    assert result is None

# edge_case - add_item - Test that add_item raises an error when the document is missing required fields.
def test_add_item_missing_fields(db_connector, mock_collection):
    mock_collection.insert_one.side_effect = Exception('ValidationError')
    with pytest.raises(Exception) as exc_info:
        db_connector.add_item('test_collection', {})
    assert 'ValidationError' in str(exc_info.value)

# edge_case - update_item - Test that update_item does not modify any document if the key-value pair does not match any document.
def test_update_item_no_match(db_connector, mock_update_one, mock_collection):
    mock_update_one.modified_count = 0
    result = db_connector.update_item('test_collection', 'name', 'non_existent_item', {'name': 'new_name'})
    mock_collection.update_one.assert_called_once_with({'name': 'non_existent_item'}, {'$set': {'name': 'new_name'}})
    assert mock_update_one.modified_count == 0

# edge_case - get_database - Test that get_database handles missing environment variables gracefully.
def test_get_database_missing_env_vars():
    with patch.dict(os.environ, {}, clear=True):
        from your_module import DBConnector  # Replace 'your_module' with the actual module name
        db_connector = DBConnector()
        with pytest.raises(KeyError):
            db_connector.get_database()

# edge_case - get_database - Test that the database connection is not established if MongoClient fails to connect.
def test_database_connection_failure(mock_connection_failure):
    from your_module import DBConnector  # Replace 'your_module' with the actual module name
    db_connector = DBConnector()
    with pytest.raises(ConnectionFailure):
        db_connector.get_database()

