import pytest
from unittest.mock import patch, MagicMock
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from Database.db_connect import DBConnector

load_dotenv()

@pytest.fixture
def mock_db_connector():
    with patch('Database.db_connect.MongoClient') as mock_mongo_client:
        mock_client_instance = MagicMock()
        mock_mongo_client.return_value = mock_client_instance
        mock_db = mock_client_instance["toybox"]
        mock_collection = mock_db["toys"]

        # Mock methods for collections
        mock_collection.find_one.return_value = {'name': 'Teddy Bear', 'type': 'Stuffed Animal'}
        mock_collection.insert_one.return_value.acknowledged = True
        mock_collection.update_one.return_value.matched_count = 1

        yield DBConnector()

        # Ensure all mocks are called as expected
        mock_mongo_client.assert_called_with(host=os.environ["DB_HOST"], port=int(os.environ["DB_PORT"]))
        mock_client_instance["toybox"].assert_called()
        mock_db["toys"].assert_called()

# happy_path - test_get_item_valid_key_value - Test that get_item retrieves a document with the specified key-value pair from the collection.
def test_get_item_valid_key_value(mock_db_connector):
    result = mock_db_connector.get_item('toys', 'name', 'Teddy Bear')
    assert result == {'name': 'Teddy Bear', 'type': 'Stuffed Animal'}

# happy_path - test_add_item_valid_document - Test that add_item inserts a document into the specified collection and returns the inserted item.
def test_add_item_valid_document(mock_db_connector):
    document = {'name': 'Lego Set', 'pieces': 500}
    result = mock_db_connector.add_item('toys', document)
    assert result.acknowledged is True

# happy_path - test_update_item_valid_key_value - Test that update_item modifies a document with the specified key-value pair by applying the update dictionary.
def test_update_item_valid_key_value(mock_db_connector):
    update_dict = {'price': 19.99}
    result = mock_db_connector.update_item('toys', 'name', 'Teddy Bear', update_dict)
    assert result == {'price': 19.99}

# happy_path - test_get_database_initialization - Test that get_database initializes the database client and sets the database to 'toybox'.
def test_get_database_initialization(mock_db_connector):
    mock_db_connector.get_database()
    assert mock_db_connector.database.name == 'toybox'

# happy_path - test_add_item_insert_one_result - Test that add_item returns an InsertOneResult object after inserting a document.
def test_add_item_insert_one_result(mock_db_connector):
    document = {'name': "Rubik's Cube", 'difficulty': 'Medium'}
    result = mock_db_connector.add_item('toys', document)
    assert isinstance(result, MagicMock)

# edge_case - test_get_item_nonexistent_key_value - Test that get_item returns None if the key-value pair does not exist in the collection.
def test_get_item_nonexistent_key_value(mock_db_connector):
    mock_db_connector.get_item('toys', 'name', 'Nonexistent Toy')
    mock_db_connector.database['toys'].find_one.assert_called_with({'name': 'Nonexistent Toy'})
    assert mock_db_connector.database['toys'].find_one.return_value is None

# edge_case - test_add_item_missing_fields - Test that add_item raises an error when inserting a document without required fields.
def test_add_item_missing_fields(mock_db_connector):
    document = {'name': 'Incomplete Toy'}
    with pytest.raises(Exception) as exc_info:
        mock_db_connector.add_item('toys', document)
    assert 'MissingRequiredFieldsError' in str(exc_info.value)

# edge_case - test_update_item_nonexistent_key_value - Test that update_item does not modify any document if the key-value pair does not match any document.
def test_update_item_nonexistent_key_value(mock_db_connector):
    update_dict = {'price': 9.99}
    mock_db_connector.update_item('toys', 'name', 'Nonexistent Toy', update_dict)
    assert mock_db_connector.database['toys'].update_one.return_value.matched_count == 0

# edge_case - test_get_database_invalid_host - Test that get_database raises a connection error if the database host is incorrect.
def test_get_database_invalid_host(mock_db_connector):
    with patch.dict(os.environ, {"DB_HOST": "invalid_host"}):
        with pytest.raises(Exception) as exc_info:
            mock_db_connector.get_database()
        assert 'ConnectionError' in str(exc_info.value)

# edge_case - test_update_item_empty_update_dict - Test that update_item raises an error when update_dict is empty.
def test_update_item_empty_update_dict(mock_db_connector):
    with pytest.raises(Exception) as exc_info:
        mock_db_connector.update_item('toys', 'name', 'Teddy Bear', {})
    assert 'EmptyUpdateDictError' in str(exc_info.value)

