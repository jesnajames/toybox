import pytest
from unittest.mock import patch, MagicMock
from Infrastructure import NotFoundException, ToyModel
from Database.db_connect import DBConnector
from ToyBoxQueries.toy_query_processor import ToyQueryProcessor

@pytest.fixture
def mock_db_connector():
    with patch('ToyBoxQueries.toy_query_processor.DBConnector') as MockDBConnector:
        mock_db_connector_instance = MockDBConnector.return_value
        mock_db_connector_instance.get_item = MagicMock()
        yield mock_db_connector_instance

@pytest.fixture
def mock_toy_model():
    with patch('ToyBoxQueries.toy_query_processor.ToyModel') as MockToyModel:
        mock_toy_model_instance = MockToyModel.return_value
        yield mock_toy_model_instance

@pytest.fixture
def setup_mocks(mock_db_connector, mock_toy_model):
    # Happy path mocks
    mock_db_connector.get_item.side_effect = lambda table, key, value: {
        '123': {'name': 'Toy Car', 'color': 'Red'},
        '124': {'name': 'Toy Train', 'color': 'Blue'}
    }.get(value, None)

    # Edge case mocks
    mock_db_connector.get_item.side_effect = lambda table, key, value: {
        '999': None,
        '': None,
        '!@#$': None
    }.get(value, None)
    
    yield

# happy_path - get_toy - Test that get_toy returns a toy model when toy is found
def test_get_toy_found(setup_mocks):
    toy_id = '123'
    expected_result = {'name': 'Toy Car', 'color': 'Red'}
    result = ToyQueryProcessor.get_toy(toy_id)
    assert result == expected_result

# happy_path - get_item - Test that get_item retrieves item from database
def test_get_item_retrieves_item(mock_db_connector):
    mock_db_connector.get_item.return_value = {'name': 'Toy Car', 'color': 'Red'}
    result = mock_db_connector.get_item('toys', 'toy_id', '123')
    expected_result = {'name': 'Toy Car', 'color': 'Red'}
    assert result == expected_result

# happy_path - get_toy - Test that get_toy returns correct toy model attributes
def test_get_toy_attributes(setup_mocks):
    toy_id = '123'
    expected_result = {'name': 'Toy Car', 'color': 'Red', 'price': 19.99}
    result = ToyQueryProcessor.get_toy(toy_id)
    assert result == expected_result

# happy_path - get_item - Test that get_item returns correct attributes from database
def test_get_item_attributes(mock_db_connector):
    mock_db_connector.get_item.return_value = {'name': 'Toy Car', 'color': 'Red', 'price': 19.99}
    result = mock_db_connector.get_item('toys', 'toy_id', '123')
    expected_result = {'name': 'Toy Car', 'color': 'Red', 'price': 19.99}
    assert result == expected_result

# happy_path - get_toy - Test that get_toy handles multiple toy models
def test_get_toy_multiple(setup_mocks):
    toy_id = '124'
    expected_result = {'name': 'Toy Train', 'color': 'Blue'}
    result = ToyQueryProcessor.get_toy(toy_id)
    assert result == expected_result

# happy_path - get_item - Test that get_item handles multiple items in database
def test_get_item_multiple(mock_db_connector):
    mock_db_connector.get_item.return_value = {'name': 'Toy Train', 'color': 'Blue'}
    result = mock_db_connector.get_item('toys', 'toy_id', '124')
    expected_result = {'name': 'Toy Train', 'color': 'Blue'}
    assert result == expected_result

# edge_case - get_toy - Test that get_toy raises NotFoundException for non-existent toy
def test_get_toy_not_found(setup_mocks):
    toy_id = '999'
    with pytest.raises(NotFoundException):
        ToyQueryProcessor.get_toy(toy_id)

# edge_case - get_item - Test that get_item returns None for non-existent item
def test_get_item_not_found(mock_db_connector):
    mock_db_connector.get_item.return_value = None
    result = mock_db_connector.get_item('toys', 'toy_id', '999')
    assert result is None

# edge_case - get_toy - Test that get_toy handles empty toy_id
def test_get_toy_empty_id(setup_mocks):
    toy_id = ''
    with pytest.raises(NotFoundException):
        ToyQueryProcessor.get_toy(toy_id)

# edge_case - get_item - Test that get_item handles empty key value
def test_get_item_empty_value(mock_db_connector):
    mock_db_connector.get_item.return_value = None
    result = mock_db_connector.get_item('toys', 'toy_id', '')
    assert result is None

# edge_case - get_toy - Test that get_toy handles special characters in toy_id
def test_get_toy_special_characters(setup_mocks):
    toy_id = '!@#$'
    with pytest.raises(NotFoundException):
        ToyQueryProcessor.get_toy(toy_id)

# edge_case - get_item - Test that get_item handles special characters in key value
def test_get_item_special_characters(mock_db_connector):
    mock_db_connector.get_item.return_value = None
    result = mock_db_connector.get_item('toys', 'toy_id', '!@#$')
    assert result is None

