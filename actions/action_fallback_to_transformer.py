# actions/action_fallback_to_transformer.py
'''
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from typing import Any, Dict, List
import requests
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class ActionFallbackToTransformer(Action):
    def name(self) -> str:
        return "action_fallback_to_transformer"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[str, Any]
    ) -> List[Dict[str, Any]]:

        user_msg = tracker.latest_message.get("text", "").strip()

        if not user_msg:
            fallback_reply = "Sorry, I didn’t catch that. Could you please rephrase?"
            dispatcher.utter_message(text=fallback_reply)
            return []

        logger.info(f"[Transformer Fallback] User message: '{user_msg}'")

        payload = {
            "model": "mistral",
            "prompt": f"You are an expert electronics assistant. Answer this: {user_msg}",
            "stream": False
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json=payload,
                headers=headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            api_answer = data.get("response", "Sorry, I don’t know that one.")
        except requests.RequestException as e:
            logger.error(f"[Transformer Fallback Error] Request failed: {e}")
            api_answer = "Sorry, I’m having trouble answering that right now."
        except ValueError:
            logger.error("[Transformer Fallback Error] Invalid JSON response.")
            api_answer = "Sorry, I didn’t understand the response from my assistant."

        custom_suffix = (
            "\n\nThis is an AI generated response. "
            "If you want to talk to a human assistant with your issue, "
            "feel free to contact our customer support desk!"
        )

        answer = api_answer.strip() + custom_suffix

        dispatcher.utter_message(text=answer)
        return []
'''
