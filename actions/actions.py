'''
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import numpy as np
from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cosine

# --- Load model once ---
MODEL = SentenceTransformer('all-MiniLM-L6-v2')

# --- Mock product database (replaceable with real DB later) ---
PRODUCTS = {
    "laptop": [
        {
            "name": "Dell XPS 13",
            "brand": "Dell",
            "stock": 5,
            "price": 999,
            "offers": "10% off",
            "description": "Compact, portable laptop with excellent battery life, ideal for professionals and students."
        },
        {
            "name": "MacBook Pro",
            "brand": "Apple",
            "stock": 0,
            "price": 1299,
            "offers": "No current offers",
            "description": "High-performance laptop for creative professionals with macOS and Retina display."
        },
        {
            "name": "Lenovo Legion 5",
            "brand": "Lenovo",
            "stock": 3,
            "price": 1200,
            "offers": "5% off",
            "description": "Powerful gaming laptop with high-end graphics, suitable for gamers but less portable."
        },
        {
            "name": "HP Spectre x360",
            "brand": "HP",
            "stock": 4,
            "price": 1399,
            "offers": "15% off",
            "description": "2-in-1 convertible laptop with touchscreen and lightweight design."
        },
        {
            "name": "MSI GF63 Thin",
            "brand": "MSI",
            "stock": 6,
            "price": 1099,
            "offers": "10% gaming kit bundle",
            "description": "Budget gaming laptop with dedicated graphics and sleek build."
        }
    ],
    "phone": [
        {
            "name": "Samsung Galaxy S23",
            "brand": "Samsung",
            "stock": 7,
            "price": 699,
            "offers": "15% discount",
            "description": "Flagship Samsung phone with stunning display and excellent camera quality."
        },
        {
            "name": "Samsung M31s",
            "brand": "Samsung",
            "stock": 5,
            "price": 280,
            "offers": "10% off",
            "description": "Budget smartphone with long battery life and decent camera setup."
        },
        {
            "name": "Google Pixel 7",
            "brand": "Google",
            "stock": 4,
            "price": 599,
            "offers": "No current offers",
            "description": "Pure Android experience with top-tier AI camera and clean OS."
        },
        {
            "name": "OnePlus 11",
            "brand": "OnePlus",
            "stock": 3,
            "price": 649,
            "offers": "5% discount",
            "description": "Flagship killer with fast charging, smooth UI, and great performance."
        }
    ],
    "tablet": [
        {
            "name": "Apple iPad Air",
            "brand": "Apple",
            "stock": 6,
            "price": 599,
            "offers": "5% discount",
            "description": "Lightweight tablet with Retina display and powerful performance."
        },
        {
            "name": "Samsung Galaxy Tab S7",
            "brand": "Samsung",
            "stock": 4,
            "price": 649,
            "offers": "No current offers",
            "description": "Versatile Android tablet with high refresh display and stylus support."
        }
    ],
    "bt_speaker": [
        {
            "name": "JBL Flip 5",
            "brand": "JBL",
            "stock": 10,
            "price": 120,
            "offers": "Free carrying pouch",
            "description": "Portable Bluetooth speaker with powerful sound and USB-C charging."
        },
        {
            "name": "Sony SRS-XB12",
            "brand": "Sony",
            "stock": 5,
            "price": 90,
            "offers": "No current offers",
            "description": "Compact and lightweight Bluetooth speaker with Micro-USB charging."
        },
        {
            "name": "Anker Soundcore 2",
            "brand": "Anker",
            "stock": 8,
            "price": 50,
            "offers": "10% discount",
            "description": "Affordable rugged Bluetooth speaker with long battery life."
        }
    ],
    "headphones": [
        {
            "name": "Sony WH-1000XM4",
            "brand": "Sony",
            "stock": 3,
            "price": 299,
            "offers": "5% off",
            "description": "Wireless noise-cancelling headphones with superb sound quality and comfort."
        },
        {
            "name": "Bose QuietComfort 35 II",
            "brand": "Bose",
            "stock": 5,
            "price": 279,
            "offers": "No current offers",
            "description": "Comfortable ANC headphones with balanced audio profile."
        }
    ],
    "gaming_console": [
        {
            "name": "Sony PlayStation 5",
            "brand": "Sony",
            "stock": 2,
            "price": 499,
            "offers": "Bundle with two extra controllers",
            "description": "Next-gen gaming console with immersive graphics and haptic feedback."
        },
        {
            "name": "Xbox Series X",
            "brand": "Microsoft",
            "stock": 2,
            "price": 499,
            "offers": "Free 3-month Game Pass",
            "description": "Powerful Xbox console with 4K gaming and high-speed SSD."
        }
    ],
    "smartwatch": [
        {
            "name": "Apple Watch Series 8",
            "brand": "Apple",
            "stock": 5,
            "price": 399,
            "offers": "No current offers",
            "description": "Advanced smartwatch with health tracking and water resistance."
        },
        {
            "name": "Samsung Galaxy Watch 5",
            "brand": "Samsung",
            "stock": 7,
            "price": 279,
            "offers": "10% off",
            "description": "Versatile watch with long battery life and fitness features."
        }
    ]
}

# --- Flatten and embed all products once ---
ALL_PRODUCTS = [item for category in PRODUCTS.values() for item in category]
PRODUCT_DESCRIPTIONS = [item["description"] for item in ALL_PRODUCTS]
PRODUCT_EMBEDDINGS = MODEL.encode(PRODUCT_DESCRIPTIONS, convert_to_numpy=True)

# --- Mock policies ---
POLICIES = {
    "return": (
        "You may return most new, unopened items within 30 days of delivery for a full refund. "
        "If the return is a result of our error (you received an incorrect or defective item, etc.), "
        "we will also pay the return shipping costs. To be eligible for a return, the item must be "
        "unused and in the same condition that you received it, with the original packaging. Refunds "
        "will be processed within 5–7 business days after we receive the returned item."
    ),

    "shipping": (
        "We offer standard, expedited, and next-day shipping options. Standard shipping usually takes "
        "3–5 business days. Expedited shipping delivers within 1–2 business days. Shipping charges are "
        "calculated at checkout based on your location and the items in your order. All orders are processed "
        "within 1–2 business days, and tracking information is provided as soon as your package is dispatched."
    ),

    "warranty": (
        "All electronic products come with a standard 1-year manufacturer’s warranty, covering defects in materials "
        "and workmanship under normal use. Warranty claims require the original purchase receipt. Products that are "
        "damaged due to misuse, negligence, or unauthorized repairs are not covered. For some products, extended "
        "warranty options are available at checkout."
    )
}


class ActionRecommendProduct(Action):
    def name(self) -> Text:
        return "action_recommend_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_query = tracker.latest_message.get('text', '').lower()

        query_vector = MODEL.encode(user_query, convert_to_numpy=True)

        recommendations = []
        for idx, embedding in enumerate(PRODUCT_EMBEDDINGS):
            product = ALL_PRODUCTS[idx]
            if product["stock"] <= 0:
                continue
            sim_score = 1 - cosine(query_vector, embedding)
            recommendations.append((sim_score, product))

        recommendations.sort(key=lambda x: x[0], reverse=True)
        top_recommendations = recommendations[:5]

        if not top_recommendations:
            dispatcher.utter_message(text="Sorry, I couldn’t find matching products right now.")
            return []

        response = "Here are some products based on your preferences:\n"
        for score, prod in top_recommendations:
            response += f"- {prod['name']} (${prod['price']}): {prod['offers']}\n"

        dispatcher.utter_message(text=response)
        return []


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
            if category in PRODUCTS:
                available = [item["name"] for item in PRODUCTS[category] if item["stock"] > 0]
                if available:
                    dispatcher.utter_message(text=f"Available {category}s: {', '.join(available)}")
                else:
                    dispatcher.utter_message(text=f"No {category}s in stock right now.")
            else:
                dispatcher.utter_message(text=f"No such category '{category}'.")
        else:
            dispatcher.utter_message(text="Please specify a product or category.")
        return []


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


class ActionSubmitFeedback(Action):
    def name(self) -> Text:
        return "action_submit_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        intent = tracker.latest_message["intent"].get("name")
        if intent == "positive_feedback":
            dispatcher.utter_message(text="Thank you for your kind feedback!")
        elif intent == "negative_feedback":
            dispatcher.utter_message(text="We’re sorry to hear that. Please tell us how we can improve.")
        else:
            dispatcher.utter_message(text="Thanks for your feedback!")
        return []

'''
