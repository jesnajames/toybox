import random
from Database.toys import all_toys
from Infrastructure import ToyModel, ToyPurchaseModel, NotFoundException
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

    @classmethod
    def buy_toy(cls, toy_purchase: ToyPurchaseModel):
        try:
            toy_id = toy_purchase.toy_id
            if toy_id not in all_toys:
                raise NotFoundException(f"{toy_id} in not registered")
            toy = all_toys[toy_id]
            toy["available"] = False
            toy["owner_id"] = toy_purchase.buyer_id
            toy["mrp"] = toy_purchase.selling_price
            # TODO update toy coordinates
            all_toys.update({toy_id: toy})
            return dict(toy)
        except Exception as exc:
            print(exc, traceback.format_exc())
            return {}
