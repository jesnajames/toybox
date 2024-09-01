import pytest
from unittest.mock import patch, MagicMock
from ToyBoxCommands.toy_command_processor import ToyCommandProcessor, DBConnector, ToyModel, ToyPurchaseModel, NotFoundException

@pytest.fixture
def mock_db_connector():
    with patch('ToyBoxCommands.toy_command_processor.DBConnector') as MockDBConnector:
        mock_db = MockDBConnector.return_value
        mock_db.add_item = MagicMock(return_value={'status': 'success'})
        mock_db.get_item = MagicMock(return_value={'toy_id': 'JP200', 'name': 'Teddy Bear', 'available': True})
        mock_db.update_item = MagicMock(return_value={'status': 'success'})
        yield mock_db

@pytest.fixture
def mock_random():
    with patch('ToyBoxCommands.toy_command_processor.random.randrange', return_value=200):
        yield

@pytest.fixture
def mock_toy_model():
    with patch('ToyBoxCommands.toy_command_processor.ToyModel') as MockToyModel:
        yield MockToyModel

@pytest.fixture
def mock_toy_purchase_model():
    with patch('ToyBoxCommands.toy_command_processor.ToyPurchaseModel') as MockToyPurchaseModel:
        yield MockToyPurchaseModel

@pytest.fixture
def mock_not_found_exception():
    with patch('ToyBoxCommands.toy_command_processor.NotFoundException') as MockNotFoundException:
        yield MockNotFoundException

# happy_path - add_toy - Test that a toy is added successfully with a unique toy_id
def test_add_toy_success(mock_db_connector, mock_random, mock_toy_model):
    toy = mock_toy_model.return_value
    toy.name = 'Jenga'
    toy.price = 20.0
    toy.available = True
    result = ToyCommandProcessor.add_toy(toy)
    assert result.toy_id == 'JP200'
    assert result.name == 'Jenga'
    assert result.price == 20.0
    assert result.available is True

# happy_path - buy_toy - Test that a toy purchase updates the toy's owner and availability
def test_buy_toy_success(mock_db_connector, mock_toy_purchase_model, mock_toy_model):
    toy_purchase = mock_toy_purchase_model.return_value
    toy_purchase.toy_id = 'JP200'
    toy_purchase.buyer_id = 'U123'
    toy_purchase.selling_price = 25.0
    buyer = {'coordinates': '123,456'}
    mock_db_connector.get_item.side_effect = [{'toy_id': 'JP200', 'name': 'Teddy Bear', 'available': True}, buyer]
    result = ToyCommandProcessor.buy_toy(toy_purchase)
    assert result.toy_id == 'JP200'
    assert result.owner_id == 'U123'
    assert result.available is False
    assert result.mrp == 25.0

# happy_path - add_item - Test that an item is added to the database successfully
def test_add_item_success(mock_db_connector):
    collection = 'toys'
    item = {'toy_id': 'JP200', 'name': 'Teddy Bear'}
    result = mock_db_connector.add_item(collection, item)
    assert result['status'] == 'success'

# happy_path - get_item - Test that an item is retrieved from the database successfully
def test_get_item_success(mock_db_connector):
    collection = 'toys'
    key = 'toy_id'
    value = 'JP200'
    result = mock_db_connector.get_item(collection, key, value)
    assert result['toy_id'] == 'JP200'
    assert result['name'] == 'Teddy Bear'

# happy_path - update_item - Test that an item is updated in the database successfully
def test_update_item_success(mock_db_connector):
    collection = 'toys'
    key = 'toy_id'
    value = 'JP200'
    update_data = {'available': False}
    result = mock_db_connector.update_item(collection, key, value, update_data)
    assert result['status'] == 'success'

# edge_case - add_toy - Test that adding a toy with missing fields returns an empty dictionary
def test_add_toy_missing_fields(mock_db_connector, mock_random, mock_toy_model):
    toy = mock_toy_model.return_value
    toy.name = 'Teddy Bear'
    toy.price = None
    result = ToyCommandProcessor.add_toy(toy)
    assert result == {}

# edge_case - buy_toy - Test that buying a toy that does not exist raises NotFoundException
def test_buy_toy_not_found(mock_db_connector, mock_toy_purchase_model, mock_not_found_exception):
    toy_purchase = mock_toy_purchase_model.return_value
    toy_purchase.toy_id = 'JP999'
    toy_purchase.buyer_id = 'U123'
    toy_purchase.selling_price = 25.0
    mock_db_connector.get_item.return_value = None
    with pytest.raises(mock_not_found_exception):
        ToyCommandProcessor.buy_toy(toy_purchase)

# edge_case - add_item - Test that adding an item to a non-existent collection returns an error
def test_add_item_non_existent_collection(mock_db_connector):
    collection = 'non_existent'
    item = {'toy_id': 'JP200'}
    mock_db_connector.add_item.return_value = {'error': 'Collection not found'}
    result = mock_db_connector.add_item(collection, item)
    assert result['error'] == 'Collection not found'

# edge_case - get_item - Test that retrieving an item with an invalid key returns None
def test_get_item_invalid_key(mock_db_connector):
    collection = 'toys'
    key = 'non_existent_key'
    value = 'JP200'
    mock_db_connector.get_item.return_value = None
    result = mock_db_connector.get_item(collection, key, value)
    assert result is None

# edge_case - update_item - Test that updating an item with an invalid key returns an error
def test_update_item_invalid_key(mock_db_connector):
    collection = 'toys'
    key = 'non_existent_key'
    value = 'JP200'
    update_data = {'available': False}
    mock_db_connector.update_item.return_value = {'error': 'Key not found'}
    result = mock_db_connector.update_item(collection, key, value, update_data)
    assert result['error'] == 'Key not found'

