# actions/feedback.py
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionSubmitFeedback(Action):
    def name(self) -> Text:
        return "action_submit_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message["intent"].get("name")
        if intent == "positive_feedback":
            pass
        elif intent == "negative_feedback":
            pass
        else:
            pass
        return []

