from typing import Any, Dict
from Infrastructure import NotFoundException, ToyModel
from Database.db_connect import DBConnector

class ToyQueryProcessor:
    """
    Handles retrieval of toy records from a database.
    Parameters:
        - toy_id (str): The unique identifier for the toy to look up.
    Processing Logic:
        - This uses a class method, implying it can be called without creating an instance of the class.
        - It connects to the database using `DBConnector` and retrieves a specific toy using its `toy_id`.
        - If the toy is found, it's returned as a `ToyModel` instance.
        - If the toy is not found, a `NotFoundException` is raised with an appropriate error message.
    """
    @classmethod
    def get_toy(cls, toy_id: str) -> Dict[str, Any]:
        toy = DBConnector().get_item("toys", "toy_id", toy_id)
        if toy:
            return ToyModel(**toy)
        else:
            raise NotFoundException(f"Toy {toy_id} not found")
