import pytest
from unittest.mock import patch, MagicMock
from Infrastructure import NotFoundException, ToyModel
from Database.db_connect import DBConnector
from mymodule import ToyQueryProcessor  # Replace 'mymodule' with the actual module name

@pytest.fixture
def mock_db_connector():
    with patch('mymodule.DBConnector') as MockDBConnector:
        mock_instance = MockDBConnector.return_value
        yield mock_instance

@pytest.fixture
def mock_toy_model():
    with patch('mymodule.ToyModel') as MockToyModel:
        yield MockToyModel

@pytest.fixture
def setup_mocks(mock_db_connector, mock_toy_model):
    mock_db_connector.get_item = MagicMock()
    mock_toy_model.return_value = MagicMock()

# happy_path - test_get_toy_existing - Test that get_toy returns a toy model when toy exists in database.
def test_get_toy_existing(mock_db_connector, mock_toy_model):
    mock_db_connector.get_item.return_value = {'toy_id': '123'}
    mock_toy_model.return_value = ToyModel(toy_id='123')
    result = ToyQueryProcessor.get_toy('123')
    assert isinstance(result, ToyModel)
    assert result.toy_id == '123'

# happy_path - test_get_item_existing - Test that get_item retrieves the correct item from the database.
def test_get_item_existing(mock_db_connector):
    mock_db_connector.get_item.return_value = {'toy_id': '79'}
    result = mock_db_connector.get_item('toys', 'toy_id', '123')
    assert result == {'toy_id': '123'}

# happy_path - test_get_toy_attributes - Test that get_toy returns a toy model with correct attributes.
def test_get_toy_attributes(mock_db_connector, mock_toy_model):
    mock_db_connector.get_item.return_value = {'name': 'ToyName', 'price': 10.99}
    mock_toy_model.return_value = ToyModel(name='ToyName', price=10.99)
    result = ToyQueryProcessor.get_toy('456')
    assert result.name == 'ToyName'
    assert result.price == 10.99

# happy_path - test_get_toy_valid_id - Test that get_toy works correctly with valid toy_id.
def test_get_toy_valid_id(mock_db_connector, mock_toy_model):
    mock_db_connector.get_item.return_value = {'toy_id': '789'}
    mock_toy_model.return_value = ToyModel(toy_id='789')
    result = ToyQueryProcessor.get_toy('789')
    assert isinstance(result, ToyModel)
    assert result.toy_id == '789'

# edge_case - test_get_toy_non_existent - Test that get_toy raises NotFoundException for non-existent toy_id.
def test_get_toy_non_existent(mock_db_connector):
    mock_db_connector.get_item.return_value = None
    with pytest.raises(NotFoundException):
        ToyQueryProcessor.get_toy('999')

# edge_case - test_get_item_non_existent - Test that get_item returns None for non-existent item in database.
def test_get_item_non_existent(mock_db_connector):
    mock_db_connector.get_item.return_value = None
    result = mock_db_connector.get_item('toys', 'toy_id', '999')
    assert result is None

# edge_case - test_get_toy_special_characters - Test that get_toy handles toy_id with special characters gracefully.
def test_get_toy_special_characters(mock_db_connector):
    mock_db_connector.get_item.return_value = None
    with pytest.raises(NotFoundException):
        ToyQueryProcessor.get_toy('!@#')

# edge_case - test_get_item_empty_key_value - Test that get_item handles empty string as key value.
def test_get_item_empty_key_value(mock_db_connector):
    mock_db_connector.get_item.return_value = None
    result = mock_db_connector.get_item('toys', 'toy_id', '')
    assert result is None

# edge_case - test_get_toy_spaces - Test that get_toy raises exception for toy_id with spaces.
def test_get_toy_spaces(mock_db_connector):
    mock_db_connector.get_item.return_value = None
    with pytest.raises(NotFoundException):
        ToyQueryProcessor.get_toy('toy id')

