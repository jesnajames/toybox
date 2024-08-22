import pytest
from unittest.mock import patch, MagicMock
from pydantic import BaseModel, ValidationError
from typing import Optional, List, Dict, Any
import time

# Mocking time module for consistent timestamps
@pytest.fixture
def mock_time():
    with patch('time.time', return_value=1609459200):  # Mocked time: 2021-01-01 00:00:00
        yield

# Mocking BaseModel to isolate tests from Pydantic's internal behavior
@pytest.fixture
def mock_basemodel():
    with patch('pydantic.BaseModel', autospec=True) as mock:
        yield mock

@pytest.fixture
def toy_model_data():
    return {
        "toy_id": "toy123",
        "owner_id": "owner456",
        "coordinates": "37.7749,-122.4194",
        "name": "Action Figure",
        "mrp": 29.99,
        "description": "A cool action figure.",
        "images": ["image1.png", "image2.png"],
        "weight": "200g",
        "features": ["poseable", "collectible"],
        "recommended_age": "8+",
        "dimensions": "10x5x3",
        "brand": "ToyBrand",
        "available": True,
        "rating": 4.5,
        "review_count": 150
    }

@pytest.fixture
def toy_purchase_model_data():
    return {
        "toy_id": "toy123",
        "seller_id": "seller789",
        "buyer_id": "buyer012",
        "selling_price": 25.0,
        "purchase_timestamp": 1609459200  # Mocked timestamp
    }

@pytest.fixture
def user_data():
    return {
        "user_id": "user001",
        "coordinates": "40.7128,-74.0060",
        "first_name": "John",
        "last_name": "Doe",
        "phone_number": "123-456-7890",
        "address": "123 Main St, New York, NY"
    }
```

# happy_path - toy_model - Test that a ToyModel can be created with valid parameters.
def test_toy_model_creation(toy_model_data):
    toy = ToyModel(**toy_model_data)
    assert toy.dict() == toy_model_data


