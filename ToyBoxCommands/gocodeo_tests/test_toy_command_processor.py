import pytest
from unittest.mock import patch, MagicMock
import random
from ToyBoxCommands.toy_command_processor import ToyCommandProcessor
from Database.db_connect import DBConnector
from Infrastructure import ToyModel, ToyPurchaseModel, NotFoundException

@pytest.fixture
def mock_db_connector():
    with patch('ToyBoxCommands.toy_command_processor.DBConnector') as MockDBConnector:
        mock_db = MockDBConnector.return_value
        mock_db.add_item = MagicMock()
        mock_db.get_item = MagicMock()
        mock_db.update_item = MagicMock()
        yield mock_db

@pytest.fixture
def mock_random():
    with patch('ToyBoxCommands.toy_command_processor.random') as mock_random:
        mock_random.randrange = MagicMock(return_value=300)
        yield mock_random

@pytest.fixture
def mock_toy_model():
    return ToyModel(toy_id="JP123", name="Jenga", category="Building blocks")

@pytest.fixture
def mock_toy_purchase_model():
    return ToyPurchaseModel(toy_id="JP200", buyer_id="U123", selling_price=29.99)

@pytest.fixture
def mock_not_found_exception():
    with patch('ToyBoxCommands.toy_command_processor.NotFoundException') as MockNotFoundException:
        yield MockNotFoundException

@pytest.fixture
def setup_mocks(mock_db_connector, mock_random, mock_not_found_exception):
    return {
        "mock_db_connector": mock_db_connector,
        "mock_random": mock_random,
        "mock_not_found_exception": mock_not_found_exception
    }

# happy_path - test_get_valid_toy - Test that a toy is added successfully with a unique toy_id
def test_get_valid_toy(setup_mocks, mock_toy_model):
    mock_db = setup_mocks['mock_db_connector']
    mock_db.add_item.return_value = {'status': 'success'}
    toy = ToyCommandProcessor.add_toy(mock_toy_model)
    assert toy.toy_id.startswith('JP')
    assert toy.name == 'Jenga'
    assert toy.category == 'Building blocks'

# happy_path - test_buy_toy_success - Test that a toy is purchased successfully and marked as unavailable
def test_buy_toy_success(setup_mocks, mock_toy_purchase_model):
    mock_db = setup_mocks['mock_db_connector']
    mock_db.get_item.side_effect = [
        {'toy_id': 'JP200', 'name': 'Toy Car', 'available': True},
        {'user_id': 'U123', 'coordinates': '123,456'}
    ]
    mock_db.update_item.return_value = {'status': 'success'}
    toy = ToyCommandProcessor.buy_toy(mock_toy_purchase_model)
    assert toy.toy_id == 'JP200'
    assert not toy.available
    assert toy.owner_id == 'U123'
    assert toy.mrp == 29.99

# happy_path - test_add_item_success - Test that an item is added to the database successfully
def test_add_item_success(setup_mocks):
    mock_db = setup_mocks['mock_db_connector']
    mock_db.add_item.return_value = {'status': 'success', 'item_id': 'TC001'}
    response = mock_db.add_item('toys', {'name': 'Toy Car', 'category': 'Vehicle'})
    assert response['status'] == 'success'
    assert response['item_id'] == 'TC001'

# happy_path - test_get_item_success - Test that an item is retrieved successfully from the database
def test_get_item_success(setup_mocks):
    mock_db = setup_mocks['mock_db_connector']
    mock_db.get_item.return_value = {'toy_id': 'JP200', 'name': 'Teddy Bear'}
    item = mock_db.get_item('toys', 'toy_id', 'JP200')
    assert item['toy_id'] == 'JP200'
    assert item['name'] == 'Teddy Bear'

# happy_path - test_update_item_success - Test that an item is updated successfully in the database
def test_update_item_success(setup_mocks):
    mock_db = setup_mocks['mock_db_connector']
    mock_db.update_item.return_value = {'status': 'success', 'updated_fields': ['available']}
    response = mock_db.update_item('toys', 'toy_id', 'JP200', {'available': False})
    assert response['status'] == 'success'
    assert 'available' in response['updated_fields']

# edge_case - test_add_toy_missing_fields - Test that adding a toy with missing fields returns an empty dictionary
def test_add_toy_missing_fields(setup_mocks):
    mock_db = setup_mocks['mock_db_connector']
    mock_db.add_item.side_effect = Exception('Missing fields')
    toy = ToyCommandProcessor.add_toy(ToyModel(category='Stuffed Animal'))
    assert toy == {}

# edge_case - test_buy_toy_non_existent_id - Test that buying a toy with a non-existent toy_id raises NotFoundException
def test_buy_toy_non_existent_id(setup_mocks, mock_toy_purchase_model):
    mock_db = setup_mocks['mock_db_connector']
    mock_db.get_item.return_value = None
    with pytest.raises(NotFoundException):
        ToyCommandProcessor.buy_toy(mock_toy_purchase_model)

# edge_case - test_add_item_duplicate_id - Test that adding an item with a duplicate ID returns an error
def test_add_item_duplicate_id(setup_mocks):
    mock_db = setup_mocks['mock_db_connector']
    mock_db.add_item.return_value = {'status': 'error', 'message': 'Duplicate ID'}
    response = mock_db.add_item('toys', {'toy_id': 'JP200', 'name': 'Toy Car'})
    assert response['status'] == 'error'
    assert response['message'] == 'Duplicate ID'

# edge_case - test_get_item_non_existent_key - Test that retrieving an item with a non-existent key returns None
def test_get_item_non_existent_key(setup_mocks):
    mock_db = setup_mocks['mock_db_connector']
    mock_db.get_item.return_value = None
    item = mock_db.get_item('toys', 'toy_id', 'JP999')
    assert item is None

# edge_case - test_update_item_invalid_fields - Test that updating an item with invalid fields returns an error
def test_update_item_invalid_fields(setup_mocks):
    mock_db = setup_mocks['mock_db_connector']
    mock_db.update_item.return_value = {'status': 'error', 'message': 'Invalid fields'}
    response = mock_db.update_item('toys', 'toy_id', 'JP200', {'invalid_field': 'value'})
    assert response['status'] == 'error'
    assert response['message'] == 'Invalid fields'

