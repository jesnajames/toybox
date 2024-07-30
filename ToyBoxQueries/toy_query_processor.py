from typing import Any, Dict
from Infrastructure import NotFoundException, ToyModel
from Database.db_connect import DBConnector

class ToyQueryProcessor:
    @classmethod
    def get_toy(cls, toy_id: str) -> Dict[str, Any]:
        toy = DBConnector().get_item("toys", "toy_id", toy_id)
        if toy:
            return ToyModel(**toy)
        else:
            raise NotFoundException(f"Toy {toy_id} not found")
