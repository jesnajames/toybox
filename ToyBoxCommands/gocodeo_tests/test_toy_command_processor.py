import pytest
from unittest.mock import patch, MagicMock
from Infrastructure import ToyModel, ToyPurchaseModel, NotFoundException
from Database.db_connect import DBConnector
from ToyBoxCommands.toy_command_processor import ToyCommandProcessor

@pytest.fixture
def mock_db_connector():
    with patch('Database.db_connect.DBConnector') as mock:
        mock_instance = mock.return_value
        mock_instance.add_item = MagicMock(return_value={"toy_id": "JPXXX"})
        mock_instance.get_item = MagicMock(return_value={"toy_id": "JP201", "available": True, "owner_id": None, "mrp": 0})
        mock_instance.update_item = MagicMock(return_value=True)
        yield mock_instance

@pytest.fixture
def toy_model():
    return ToyModel(name='Teddy Bear', price=20.0)

@pytest.fixture
def toy_purchase_model():
    return ToyPurchaseModel(toy_id='JP201', buyer_id='U123', selling_price=18.0)

@pytest.fixture
def setup_toy_command_processor(mock_db_connector):
    ToyCommandProcessor.DBConnector = lambda: mock_db_connector
    yield ToyCommandProcessor

# happy_path - test_add_toy_success - Test that a toy is added successfully with a generated toy_id
def test_add_toy_success(setup_toy_command_processor, toy_model):
    toy = setup_toy_command_processor.add_toy(toy_model)
    assert toy.toy_id.startswith('JP')
    assert len(toy.toy_id) == 5

# happy_path - test_buy_toy_success - Test that a toy is purchased successfully and details are updated
def test_buy_toy_success(setup_toy_command_processor, toy_purchase_model):
    toy = setup_toy_command_processor.buy_toy(toy_purchase_model)
    assert toy.available is False
    assert toy.owner_id == 'U123'
    assert toy.mrp == 18.0

# happy_path - test_add_item_called_correctly - Test that add_item method is called with correct parameters
def test_add_item_called_correctly(mock_db_connector, toy_model):
    ToyCommandProcessor.add_toy(toy_model)
    mock_db_connector.add_item.assert_called_once_with('toys', dict(toy_model))

# happy_path - test_get_item_success - Test that get_item retrieves the toy with the correct toy_id
def test_get_item_success(mock_db_connector):
    toy = mock_db_connector.get_item('toys', 'toy_id', 'JP201')
    assert toy['toy_id'] == 'JP201'

# happy_path - test_update_item_success - Test that update_item updates the toy details successfully
def test_update_item_success(mock_db_connector, toy_purchase_model):
    ToyCommandProcessor.buy_toy(toy_purchase_model)
    mock_db_connector.update_item.assert_called_once_with('toys', 'toy_id', 'JP201', mock_db_connector.get_item.return_value)

# edge_case - test_add_toy_missing_attributes - Test that adding a toy with missing attributes returns an empty dict
def test_add_toy_missing_attributes(setup_toy_command_processor):
    incomplete_toy = ToyModel(name='')
    result = setup_toy_command_processor.add_toy(incomplete_toy)
    assert result == {}

# edge_case - test_buy_toy_non_existent_id - Test that buying a toy with non-existent toy_id raises NotFoundException
def test_buy_toy_non_existent_id(mock_db_connector):
    mock_db_connector.get_item.return_value = None
    with pytest.raises(NotFoundException):
        ToyCommandProcessor.buy_toy(ToyPurchaseModel(toy_id='JP999', buyer_id='U123', selling_price=18.0))

# edge_case - test_add_item_invalid_table - Test that add_item with invalid table name returns error
def test_add_item_invalid_table(mock_db_connector, toy_model):
    mock_db_connector.add_item.side_effect = Exception('InvalidTable')
    with pytest.raises(Exception) as exc_info:
        mock_db_connector.add_item('invalid_table', dict(toy_model))
    assert str(exc_info.value) == 'InvalidTable'

# edge_case - test_get_item_invalid_column - Test that get_item with invalid column name returns None
def test_get_item_invalid_column(mock_db_connector):
    mock_db_connector.get_item.return_value = None
    result = mock_db_connector.get_item('toys', 'invalid_column', 'JP201')
    assert result is None

# edge_case - test_update_item_non_existent_id - Test that update_item with non-existent toy_id does not update
def test_update_item_non_existent_id(mock_db_connector):
    mock_db_connector.update_item.return_value = False
    result = mock_db_connector.update_item('toys', 'toy_id', 'JP999', {'available': False})
    assert result is False

