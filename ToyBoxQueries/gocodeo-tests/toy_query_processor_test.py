# happy path - behaviour on which test case will be generated using below data
def test_get_toy_happy_path(db_connector_mock, toy_query_processor):
    toy_data = {'toy_id': '123', 'name': 'ToyName', 'price': 10.99}
    db_connector_mock.get_item.return_value = toy_data
    result = toy_query_processor.get_toy('123')
    assert result == ToyModel(**toy_data)
    db_connector_mock.get_item.assert_called_once_with('toys', 'toy_id', '123')

# edge case - behaviour on which test case will be generated using below data
def test_get_toy_not_found(db_connector_mock, toy_query_processor):
    db_connector_mock.get_item.return_value = None
    with pytest.raises(NotFoundException) as exc_info:
        toy_query_processor.get_toy('999')
    assert str(exc_info.value) == 'Toy 999 not found'
    db_connector_mock.get_item.assert_called_once_with('toys', 'toy_id', '999')

