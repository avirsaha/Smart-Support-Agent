# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Dict, Text, Any, List
from rasa_sdk import Tracker, FormValidationAction, Action
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict

class ValidateLeadForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_lead_form"

    async def extract_email(
        self, dispatcher, tracker: Tracker, domain
    ) -> Dict[Text, Any]:
        last_msg = tracker.latest_message.get("text")
        if "@" in last_msg and "." in last_msg:
            return {"email": last_msg}
        dispatcher.utter_message("That doesn't look like a valid email. Can you try again?")
        return {"email": None}

class SubmitLeadForm(Action):
    def name(self) -> Text:
        return "submit_lead_form"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[Dict[Text, Any]]:
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        phone = tracker.get_slot("phone")
        dispatcher.utter_message(text=f"Thanks {name}! We will contact you at {email} or {phone}.")
        return []

