import pytest
from unittest.mock import patch, MagicMock
from pydantic import BaseModel
from Infrastructure.models import ToyModel, ToyPurchaseModel, User
import time

# Mocking the time module
time_mock = MagicMock()
time_mock.time.return_value = 1698765432

@pytest.fixture(scope='function')
def setup_mocks():
    with patch('Infrastructure.models.time', time_mock):
        yield

@pytest.fixture(scope='function')
def mock_toy_model():
    toy_model_mock = MagicMock(spec=ToyModel)
    toy_model_mock.toy_id = "123"
    toy_model_mock.owner_id = "owner_456"
    toy_model_mock.coordinates = "40.7128,-74.0060"
    toy_model_mock.name = "Super Toy"
    toy_model_mock.mrp = 29.99
    toy_model_mock.description = "A super fun toy."
    toy_model_mock.images = ["image1.jpg", "image2.jpg"]
    toy_model_mock.weight = "1.2kg"
    toy_model_mock.features = ["fun", "educational"]
    toy_model_mock.recommended_age = "3+"
    toy_model_mock.dimensions = "10x10x10"
    toy_model_mock.brand = "ToyBrand"
    toy_model_mock.available = True
    toy_model_mock.rating = 4.5
    toy_model_mock.review_count = 100
    return toy_model_mock

@pytest.fixture(scope='function')
def mock_toy_purchase_model():
    toy_purchase_model_mock = MagicMock(spec=ToyPurchaseModel)
    toy_purchase_model_mock.toy_id = "123"
    toy_purchase_model_mock.seller_id = "seller_789"
    toy_purchase_model_mock.buyer_id = "buyer_101"
    toy_purchase_model_mock.selling_price = 25.99
    toy_purchase_model_mock.purchase_timestamp = 1698765432
    return toy_purchase_model_mock

@pytest.fixture(scope='function')
def mock_user_model():
    user_model_mock = MagicMock(spec=User)
    user_model_mock.user_id = "user_202"
    user_model_mock.coordinates = "34.0522,-118.2437"
    user_model_mock.first_name = "John"
    user_model_mock.last_name = "Doe"
    user_model_mock.phone_number = "123-456-7890"
    user_model_mock.address = "123 Main St, Anytown, USA"
    return user_model_mock

# happy_path - test_create_toy_model_with_valid_data - Test that ToyModel can be created with all valid fields.
def test_create_toy_model_with_valid_data(mock_toy_model):
    toy = ToyModel(
        toy_id=mock_toy_model.toy_id,
        owner_id=mock_toy_model.owner_id,
        coordinates=mock_toy_model.coordinates,
        name=mock_toy_model.name,
        mrp=mock_toy_model.mrp,
        description=mock_toy_model.description,
        images=mock_toy_model.images,
        weight=mock_toy_model.weight,
        features=mock_toy_model.features,
        recommended_age=mock_toy_model.recommended_age,
        dimensions=mock_toy_model.dimensions,
        brand=mock_toy_model.brand,
        available=mock_toy_model.available,
        rating=mock_toy_model.rating,
        review_count=mock_toy_model.review_count
    )
    assert toy.toy_id == "123"

# happy_path - test_create_toy_purchase_model_with_valid_data - Test that ToyPurchaseModel can be created with all valid fields.
def test_create_toy_purchase_model_with_valid_data(mock_toy_purchase_model):
    purchase = ToyPurchaseModel(
        toy_id=mock_toy_purchase_model.toy_id,
        seller_id=mock_toy_purchase_model.seller_id,
        buyer_id=mock_toy_purchase_model.buyer_id,
        selling_price=mock_toy_purchase_model.selling_price,
        purchase_timestamp=mock_toy_purchase_model.purchase_timestamp
    )
    assert purchase.toy_id == "123"

# happy_path - test_create_user_model_with_valid_data - Test that User model can be created with all valid fields.
def test_create_user_model_with_valid_data(mock_user_model):
    user = User(
        user_id=mock_user_model.user_id,
        coordinates=mock_user_model.coordinates,
        first_name=mock_user_model.first_name,
        last_name=mock_user_model.last_name,
        phone_number=mock_user_model.phone_number,
        address=mock_user_model.address
    )
    assert user.user_id == "user_202"

# happy_path - test_create_toy_model_with_optional_fields_empty - Test that ToyModel accepts empty strings for optional fields.
def test_create_toy_model_with_optional_fields_empty():
    toy = ToyModel(
        toy_id='',
        owner_id='owner_456',
        coordinates='40.7128,-74.0060',
        name='Super Toy',
        mrp=29.99,
        description='A super fun toy.',
        images=['image1.jpg', 'image2.jpg'],
        weight='1.2kg',
        features=['fun', 'educational'],
        recommended_age='3+',
        dimensions='10x10x10',
        brand='ToyBrand',
        available=True,
        rating=4.5,
        review_count=100
    )
    assert toy.toy_id == ''

# happy_path - test_create_toy_purchase_model_with_default_timestamp - Test that ToyPurchaseModel defaults purchase_timestamp to current time if not provided.
def test_create_toy_purchase_model_with_default_timestamp(setup_mocks):
    purchase = ToyPurchaseModel(
        toy_id='123',
        seller_id='seller_789',
        buyer_id='buyer_101',
        selling_price=25.99
    )
    assert purchase.purchase_timestamp == 1698765432

# edge_case - test_toy_model_missing_mandatory_fields - Test that ToyModel raises validation error for missing mandatory fields.
def test_toy_model_missing_mandatory_fields():
    with pytest.raises(ValueError):
        ToyModel(
            owner_id='',
            coordinates='',
            name='',
            description='',
            images=[],
            weight='',
            features=[],
            recommended_age='',
            dimensions='',
            brand='',
            available=False,
            rating=0.0,
            review_count=0.0
        )

# edge_case - test_toy_purchase_model_negative_selling_price - Test that ToyPurchaseModel raises error for negative selling price.
def test_toy_purchase_model_negative_selling_price():
    with pytest.raises(ValueError):
        ToyPurchaseModel(
            toy_id='123',
            seller_id='seller_789',
            buyer_id='buyer_101',
            selling_price=-25.99
        )

# edge_case - test_user_model_missing_mandatory_fields - Test that User model raises validation error for missing mandatory fields.
def test_user_model_missing_mandatory_fields():
    with pytest.raises(ValueError):
        User(
            user_id='',
            coordinates='',
            first_name='',
            last_name='',
            phone_number='',
            address=''
        )

# edge_case - test_toy_model_large_number_of_images - Test that ToyModel handles large number of images gracefully.
def test_toy_model_large_number_of_images():
    images = ['image{}.jpg'.format(i) for i in range(1000)]
    toy = ToyModel(
        toy_id='123',
        owner_id='owner_456',
        coordinates='40.7128,-74.0060',
        name='Super Toy',
        mrp=29.99,
        description='A super fun toy.',
        images=images,
        weight='1.2kg',
        features=['fun', 'educational'],
        recommended_age='3+',
        dimensions='10x10x10',
        brand='ToyBrand',
        available=True,
        rating=4.5,
        review_count=100
    )
    assert len(toy.images) == 1000

# edge_case - test_toy_purchase_model_future_timestamp - Test that ToyPurchaseModel handles future timestamp correctly.
def test_toy_purchase_model_future_timestamp():
    purchase = ToyPurchaseModel(
        toy_id='123',
        seller_id='seller_789',
        buyer_id='buyer_101',
        selling_price=25.99,
        purchase_timestamp=9999999999
    )
    assert purchase.purchase_timestamp == 9999999999

