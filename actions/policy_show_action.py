# actions/policies.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .utils import POLICIES

class ActionShowPolicy(Action):
    def name(self) -> Text:
        return "action_show_policy"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        policy_type = next(tracker.get_latest_entity_values("policy_type"), None)
        if policy_type and policy_type.lower() in POLICIES:
            dispatcher.utter_message(text=POLICIES[policy_type.lower()])
        else:
            dispatcher.utter_message(text="Which policy do you want to know about? (return, shipping, warranty)")
        return []

