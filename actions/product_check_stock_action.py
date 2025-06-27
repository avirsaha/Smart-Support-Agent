# actions/stock.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .utils import ALL_PRODUCTS

class ActionCheckStock(Action):
    def name(self) -> Text:
        return "action_check_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        product = next(tracker.get_latest_entity_values("product"), None)
        category = next(tracker.get_latest_entity_values("category"), None)

        if product:
            for prod in ALL_PRODUCTS:
                if product.lower() in prod["name"].lower():
                    stock = prod["stock"]
                    if stock > 0:
                        dispatcher.utter_message(text=f"{prod['name']} is in stock: {stock} units available.")
                    else:
                        dispatcher.utter_message(text=f"{prod['name']} is out of stock.")
                    return []
            dispatcher.utter_message(text=f"Product '{product}' not found.")

        elif category:
            category = category.lower()
            available = [
                item["name"] for item in ALL_PRODUCTS
                if item.get("category", "").lower() == category and item.get("stock", 0) > 0
            ]
            if available:
                dispatcher.utter_message(text=f"Available {category}s: {', '.join(available)}")
            else:
                dispatcher.utter_message(text=f"No {category}s in stock right now.")
        else:
            dispatcher.utter_message(text="Please specify a product or category.")

        return []

