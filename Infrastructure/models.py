from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import time

class ToyModel(BaseModel):
    toy_id: Optional[str] = ""
    owner_id: str
    coordinates: str
    name: str
    mrp: float = 0.0
    description: str
    images: List[str]
    weight: str
    features: List[str]
    recommended_age: str
    dimensions: str
    brand: str
    available: bool
    rating: float
    review_count: float


class ToyPurchaseModel(BaseModel):
    toy_id: str
    seller_id: str
    buyer_id: str
    selling_price: float
    purchase_timestamp: int = int(time.time())


class User(BaseModel):
    user_id: str
    coordinates: str
    first_name: str
    last_name: str
    phone_number: str
    address: str
