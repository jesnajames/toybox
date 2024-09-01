import pytest
from unittest import mock
from ToyBoxCommands.toy_command_processor import ToyCommandProcessor
from Database.db_connect import DBConnector
from Infrastructure import ToyModel, ToyPurchaseModel, NotFoundException

@pytest.fixture
def mock_db_connector():
    with mock.patch('ToyBoxCommands.toy_command_processor.DBConnector') as MockDBConnector:
        mock_instance = MockDBConnector.return_value
        mock_instance.add_item.return_value = {'status': 'success'}
        mock_instance.get_item.return_value = {'toy_id': 'JP201', 'name': 'Teddy Bear', 'available': True, 'owner_id': None, 'mrp': None, 'coordinates': '10,10'}
        mock_instance.update_item.return_value = {'status': 'success'}
        yield MockDBConnector

@pytest.fixture
def mock_random():
    with mock.patch('ToyBoxCommands.toy_command_processor.random') as MockRandom:
        MockRandom.randrange.return_value = 201
        yield MockRandom

@pytest.fixture
def toy_model():
    return ToyModel(name='Teddy Bear', category='Stuffed Animals')

@pytest.fixture
def toy_purchase_model():
    return ToyPurchaseModel(toy_id='JP201', buyer_id='user123', selling_price=19.99)

@pytest.fixture
def mock_traceback():
    with mock.patch('ToyBoxCommands.toy_command_processor.traceback') as MockTraceback:
        MockTraceback.format_exc.return_value = 'Traceback (most recent call last): ...'
        yield MockTraceback

# happy_path - test_add_toy_success - Test that a toy is successfully added with a generated toy_id
def test_add_toy_success(mock_db_connector, mock_random, toy_model):
    result = ToyCommandProcessor.add_toy(toy_model)
    assert result.toy_id.startswith('JP')
    assert result.name == 'Teddy Bear'
    assert result.category == 'Stuffed Animals'

# happy_path - test_buy_toy_success - Test that a toy purchase updates the toy's owner and availability
def test_buy_toy_success(mock_db_connector, toy_purchase_model):
    result = ToyCommandProcessor.buy_toy(toy_purchase_model)
    assert result.toy_id == 'JP201'
    assert result.available is False
    assert result.owner_id == 'user123'
    assert result.mrp == 19.99

# happy_path - test_randrange_within_bounds - Test that random.randrange generates a number within the expected range
def test_randrange_within_bounds(mock_random):
    number = random.randrange(200, 500)
    assert 200 <= number < 500

# happy_path - test_add_item_success - Test that an item is added to the database successfully
def test_add_item_success(mock_db_connector, toy_model):
    result = DBConnector().add_item('toys', dict(toy_model))
    assert result['status'] == 'success'

# happy_path - test_get_item_success - Test that an item is retrieved from the database successfully
def test_get_item_success(mock_db_connector):
    result = DBConnector().get_item('toys', 'toy_id', 'JP201')
    assert result['toy_id'] == 'JP201'
    assert result['name'] == 'Teddy Bear'

# happy_path - test_update_item_success - Test that an item is updated in the database successfully
def test_update_item_success(mock_db_connector):
    update_data = {'available': False}
    result = DBConnector().update_item('toys', 'toy_id', 'JP201', update_data)
    assert result['status'] == 'success'

# edge_case - test_add_toy_missing_fields - Test that adding a toy with missing fields returns an error
def test_add_toy_missing_fields(mock_db_connector):
    incomplete_toy = ToyModel(category='Stuffed Animals')
    result = ToyCommandProcessor.add_toy(incomplete_toy)
    assert 'error' in result

# edge_case - test_buy_toy_invalid_id - Test that buying a toy with an invalid toy_id raises NotFoundException
def test_buy_toy_invalid_id(mock_db_connector):
    mock_db_connector.return_value.get_item.return_value = None
    toy_purchase = ToyPurchaseModel(toy_id='JP999', buyer_id='user123', selling_price=19.99)
    result = ToyCommandProcessor.buy_toy(toy_purchase)
    assert 'exception' in result

# edge_case - test_randrange_invalid_range - Test that random.randrange with invalid range raises ValueError
def test_randrange_invalid_range(mock_random):
    with pytest.raises(ValueError):
        random.randrange(500, 200)

# edge_case - test_add_item_duplicate_id - Test that adding an item with an existing ID returns an error
def test_add_item_duplicate_id(mock_db_connector):
    mock_db_connector.return_value.add_item.side_effect = Exception('Duplicate ID')
    toy = ToyModel(toy_id='JP201', name='Robot')
    result = DBConnector().add_item('toys', dict(toy))
    assert 'error' in result

# edge_case - test_get_item_non_existent - Test that retrieving a non-existent item returns None
def test_get_item_non_existent(mock_db_connector):
    mock_db_connector.return_value.get_item.return_value = None
    result = DBConnector().get_item('toys', 'toy_id', 'JP999')
    assert result is None

# edge_case - test_update_item_non_existent - Test that updating a non-existent item returns an error
def test_update_item_non_existent(mock_db_connector):
    mock_db_connector.return_value.update_item.side_effect = Exception('Item not found')
    update_data = {'available': False}
    result = DBConnector().update_item('toys', 'toy_id', 'JP999', update_data)
    assert 'error' in result

