# happy path - get_toy
def test_get_toy_happy_path(toy_query_processor_test_setup):
    toy_data = {'toy_id': '123', 'name': 'ToyName', 'price': 10.99}
    toy_query_processor_test_setup.get_item.return_value = toy_data
    result = ToyQueryProcessor.get_toy('123')
    assert result.toy_id == '123'
    assert result.name == 'ToyName'
    assert result.price == 10.99
    toy_query_processor_test_setup.get_item.assert_called_once_with('toys', 'toy_id', '123')

# edge case - get_toy
def test_get_toy_not_found(toy_query_processor_test_setup):
    toy_query_processor_test_setup.get_item.return_value = None
    with pytest.raises(NotFoundException) as exc_info:
        ToyQueryProcessor.get_toy('999')
    assert str(exc_info.value) == 'Toy 999 not found'
    toy_query_processor_test_setup.get_item.assert_called_once_with('toys', 'toy_id', '999')

