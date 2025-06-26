from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# Mock database
PRODUCTS = {
    "laptop": [
        {"name": "Dell XPS 13", "stock": 5, "price": 999, "offers": "10% off"},
        {"name": "MacBook Pro", "stock": 0, "price": 1299, "offers": "No current offers"}
    ],
    "phone": [
        {"name": "iPhone 14", "stock": 10, "price": 799, "offers": "Free AirPods with purchase"},
        {"name": "Samsung Galaxy S23", "stock": 7, "price": 699, "offers": "15% discount"}
    ],
    "headphones": [
        {"name": "Sony WH-1000XM4", "stock": 3, "price": 299, "offers": "5% off"}
    ]
}

# Mock policies
POLICIES = {
    "return": (
        "We want you to be completely satisfied with your purchase. If for any reason you are not, "
        "you may return the item within 30 calendar days from the date of purchase. To be eligible "
        "for a return, the item must be in its original condition, unused, and in the original packaging. "
        "Please ensure you have a valid receipt or proof of purchase to process the return smoothly. "
        "Returns may be subject to inspection upon receipt, and some items may be excluded from return "
        "eligibility as per their specific terms and conditions."
    ),
    "shipping": (
        "Our standard shipping option typically delivers your order within 3 to 5 business days, depending "
        "on your location and the availability of the items ordered. We also offer express shipping for "
        "those who require faster delivery, which can shorten delivery times to 1 to 2 business days. "
        "Shipping charges and delivery times may vary based on the shipping method selected at checkout, "
        "the size and weight of the package, and your shipping address. Tracking information will be provided "
        "once your order has been dispatched."
    ),
    "warranty": (
        "Most of the products we sell include a standard manufacturer’s warranty valid for one year from the "
        "date of purchase. This warranty covers defects in materials and workmanship under normal use. "
        "If a defect arises and a valid claim is received within the warranty period, we will repair or replace "
        "the product at no charge. Additionally, we offer an extended warranty option on select items, which "
        "can be purchased separately to provide coverage beyond the standard warranty period. Please refer "
        "to the specific product warranty details for more information."
    )
}

class ActionCheckStock(Action):
    def name(self) -> Text:
        return "action_check_stock"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        product = next(tracker.get_latest_entity_values("product"), None)
        category = next(tracker.get_latest_entity_values("category"), None)

        if product:
            for cat, items in PRODUCTS.items():
                for item in items:
                    if product.lower() in item["name"].lower():
                        stock = item["stock"]
                        if stock > 0:
                            dispatcher.utter_message(text=f"Yes, the {item['name']} is in stock with {stock} units available.")
                        else:
                            dispatcher.utter_message(text=f"Sorry, the {item['name']} is currently out of stock.")
                        return []
            dispatcher.utter_message(text=f"Sorry, I couldn't find the product '{product}'.")
        elif category:
            if category.lower() in PRODUCTS:
                available = [item["name"] for item in PRODUCTS[category.lower()] if item["stock"] > 0]
                if available:
                    dispatcher.utter_message(text=f"We have the following {category}s in stock: {', '.join(available)}.")
                else:
                    dispatcher.utter_message(text=f"Currently, we have no {category}s in stock.")
            else:
                dispatcher.utter_message(text=f"Sorry, we don't have the category '{category}'.")
        else:
            dispatcher.utter_message(text="Please specify the product or category you want to check.")
        
        return []

class ActionCheckOffer(Action):
    def name(self) -> Text:
        return "action_check_offer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        category = next(tracker.get_latest_entity_values("category"), None)
        product = next(tracker.get_latest_entity_values("product"), None)

        offers = []
        if product:
            for cat, items in PRODUCTS.items():
                for item in items:
                    if product.lower() in item["name"].lower():
                        offers.append(f"{item['name']}: {item['offers']}")
        elif category:
            if category.lower() in PRODUCTS:
                for item in PRODUCTS[category.lower()]:
                    offers.append(f"{item['name']}: {item['offers']}")
            else:
                dispatcher.utter_message(text=f"Sorry, we don't have offers for the category '{category}'.")
                return []
        else:
            for cat, items in PRODUCTS.items():
                for item in items:
                    if item['offers'] and "No current offers" not in item['offers']:
                        offers.append(f"{item['name']}: {item['offers']}")

        if offers:
            dispatcher.utter_message(text="Here are some current offers:\n" + "\n".join(offers))
        else:
            dispatcher.utter_message(text="Sorry, there are no current offers at the moment.")
        return []

class ActionRecommendProduct(Action):
    def name(self) -> Text:
        return "action_recommend_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_msg = tracker.latest_message.get('text', '').lower()

        if "gaming" in user_msg:
            recs = [item["name"] for item in PRODUCTS.get("laptop", []) if "gaming" in item["name"].lower()]
            if not recs:
                recs = ["Dell XPS 13", "MacBook Pro"]
        elif "photography" in user_msg:
            recs = ["Canon EOS 90D", "Nikon D5600"]  # mock outside PRODUCTS
        elif "budget" in user_msg:
            recs = [item["name"] for item in PRODUCTS.get("phone", []) if item["price"] < 700]
        else:
            recs = ["Dell XPS 13", "iPhone 14", "Sony WH-1000XM4"]

        dispatcher.utter_message(text=f"I recommend these products: {', '.join(recs)}.")
        return []

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
            dispatcher.utter_message(text="Please specify which policy you want to know about: return, shipping, or warranty.")
        return []

class ActionAskAvailableProducts(Action):
    def name(self) -> Text:
        return "action_ask_available_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        all_products = []
        for items in PRODUCTS.values():
            for item in items:
                all_products.append(item["name"])
        
        if all_products:
            dispatcher.utter_message(text="Here are some products you can explore:\n" + "\n".join(all_products))
        else:
            dispatcher.utter_message(text="Sorry, there are currently no products available.")
        return []

class ActionSubmitFeedback(Action):
    def name(self) -> Text:
        return "action_submit_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message["intent"].get("name")

        if intent == "positive_feedback":
            dispatcher.utter_message(text="Thank you for your kind feedback! We're glad you're satisfied.")
        elif intent == "negative_feedback":
            dispatcher.utter_message(text="We’re sorry to hear that. Could you share more details so we can improve?")
        else:
            dispatcher.utter_message(text="Thanks for your feedback!")
        return []
