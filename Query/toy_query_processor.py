from typing import Any, Dict
from Infrastructure import NotFoundException
from Database.toys import all_toys


class ToyQueryProcessor:
    @classmethod
    def get_toy(cls, toy_id: str) -> Dict[str, Any]:
        if toy_id in all_toys:
            return all_toys[toy_id]
        else:
            raise NotFoundException(f"Toy {toy_id} not found")
