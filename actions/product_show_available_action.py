# actions/catalog.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .utils import ALL_PRODUCTS

class ActionAskAvailableProducts(Action):
    def name(self) -> Text:
        return "action_ask_available_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        names = [p["name"] for p in ALL_PRODUCTS if p["stock"] > 0]
        if names:
            dispatcher.utter_message(text="Available products:\n" + "\n".join(names))
        else:
            dispatcher.utter_message(text="Sorry, no products currently in stock.")
        return []

