from pydantic import BaseModel
from typing import Optional, List, Dict, Any


class ToyModel(BaseModel):
    toy_id: Optional[str] = ""
    owner_id: str
    coordinates: str
    name: str
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
