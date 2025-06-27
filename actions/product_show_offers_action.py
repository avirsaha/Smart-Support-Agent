# actions/offers.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .utils import ALL_PRODUCTS

class ActionCheckOffer(Action):
    def name(self) -> Text:
        return "action_check_offer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        offers = []
        for prod in ALL_PRODUCTS:
            if prod["stock"] > 0 and "no current offers" not in prod["offers"].lower():
                offers.append(f"{prod['name']}: {prod['offers']}")

        if offers:
            dispatcher.utter_message(text="Current offers:\n" + "\n".join(offers))
        else:
            dispatcher.utter_message(text="There are no current offers.")
        return []

