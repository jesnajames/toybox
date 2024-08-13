# happy path - add_toy
def test_add_toy_success(toy_command_processor, db_connector_mock):
    toy = ToyModel(name='Toy1', price=100)
    db_connector_mock.add_item.return_value = toy
    result = toy_command_processor.add_toy(toy)
    assert result.toy_id.startswith('JP')
    assert result.name == 'Toy1'
    assert result.price == 100

# happy path - buy_toy
def test_buy_toy_success(toy_command_processor, db_connector_mock):
    toy_purchase = ToyPurchaseModel(toy_id='JP201', buyer_id='user123', selling_price=150)
    toy_data = {'toy_id': 'JP201', 'name': 'Toy1', 'price': 100, 'available': True}
    user_data = {'user_id': 'user123', 'coordinates': '123,456'}
    db_connector_mock.get_item.side_effect = [toy_data, user_data]
    result = toy_command_processor.buy_toy(toy_purchase)
    assert result.toy_id == 'JP201'
    assert result.owner_id == 'user123'
    assert result.mrp == 150
    assert result.coordinates == '123,456'

# edge case - buy_toy
def test_buy_toy_toy_not_found(toy_command_processor, db_connector_mock):
    toy_purchase = ToyPurchaseModel(toy_id='JP201', buyer_id='user123', selling_price=150)
    db_connector_mock.get_item.return_value = None
    result = toy_command_processor.buy_toy(toy_purchase)
    assert result == {}

# edge case - add_toy
def test_add_toy_exception(toy_command_processor, db_connector_mock):
    toy = ToyModel(name='Toy1', price=100)
    db_connector_mock.add_item.side_effect = Exception('DB Error')
    result = toy_command_processor.add_toy(toy)
    assert result == {}

