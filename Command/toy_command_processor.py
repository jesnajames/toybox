import random
from Database.toys import all_toys
from Infrastructure import ToyModel
import traceback

class ToyCommandProcessor:
    @classmethod
    def add_toy(cls, toy: ToyModel):
        try:
            toy_id = f"JP{random.randrange(200,500)}"
            toy.toy_id = toy_id
            all_toys[toy_id] = dict(toy)
            return all_toys[toy_id]
        except Exception as exc:
            print(exc, traceback.format_exc())
            return {}