import random
from Database.db_connect import DBConnector
from Infrastructure import ToyModel, ToyPurchaseModel, NotFoundException
import traceback

class ToyCommandProcessor:
    @classmethod
    def add_toy(cls, toy: ToyModel):
        try:
            toy_id = f"JP{random.randrange(200,500)}"
            toy.toy_id = toy_id
            response = DBConnector().add_item("toys", dict(toy))
            return toy
        except Exception as exc:
            print(exc, traceback.format_exc())
            return {}

    @classmethod
    def buy_toy(cls, toy_purchase: ToyPurchaseModel):
        try:
            toy_id = toy_purchase.toy_id
            current_toy = DBConnector().get_item("toys", "toy_id", toy_id)
            if not current_toy:
                raise NotFoundException(f"{toy_id} in not registered")
            current_toy["available"] = False
            current_toy["owner_id"] = toy_purchase.buyer_id
            current_toy["mrp"] = toy_purchase.selling_price

            buyer = DBConnector().get_item("users", "user_id", toy_purchase.buyer_id)
            current_toy["coordinates"] = buyer.get("coordinates", "")
            DBConnector().update_item("toys", "toy_id", toy_id, current_toy)
            return ToyModel(**current_toy)
        except Exception as exc:
            print(exc, traceback.format_exc())
            return {}
