from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from .utils import ALL_PRODUCTS, PRODUCT_EMBEDDINGS, MODEL
from scipy.spatial.distance import cosine
import re

class ActionRecommendProduct(Action):
    def name(self) -> Text:
        return "action_recommend_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_message = tracker.latest_message.get("text", "").lower()
        entities = tracker.latest_message.get("entities", [])

        # Extract structured preferences
        preferences = {}
        for ent in entities:
            entity_name = ent.get("entity")
            entity_value = ent.get("value", "").lower()
            preferences[entity_name] = entity_value

        max_price = None
        min_price = None
        if "price_range" in preferences:
            price_text = preferences["price_range"]
            under = re.search(r"under\s*\₹?\$?(\d+)", price_text)
            over = re.search(r"over\s*\₹?\$?(\d+)", price_text)
            between = re.search(r"(\d+)\s*[-to]+\s*(\d+)", price_text)
            exact = re.search(r"\₹?\$?(\d+)", price_text)

            if under:
                max_price = int(under.group(1))
            elif over:
                min_price = int(over.group(1))
            elif between:
                min_price = int(between.group(1))
                max_price = int(between.group(2))
            elif exact:
                max_price = int(exact.group(1))

        # Step 1: Filter based on structured data
        candidate_products = ALL_PRODUCTS.copy()

        def match_nested_spec(spec_field, pref_key):
            pref_val = preferences.get(pref_key)
            if not pref_val:
                return True
            return pref_val in product.get("specs", {}).get(spec_field, "").lower()

        filtered = []
        for product in candidate_products:
            if product.get("stock", 0) <= 0:
                continue

            if "category" in preferences and preferences["category"] not in product["category"].lower():
                continue
            if "brand" in preferences and preferences["brand"] not in product["brand"].lower():
                continue
            if "color" in preferences and preferences["color"] not in product.get("color", "").lower():
                continue
            if max_price and product["price"] > max_price:
                continue
            if min_price and product["price"] < min_price:
                continue

            if not match_nested_spec("battery", "battery_life"): continue
            if not match_nested_spec("camera", "camera_quality"): continue
            if not match_nested_spec("display", "display_quality"): continue
            if not match_nested_spec("performance", "performance"): continue
            if not match_nested_spec("storage", "storage"): continue

            filtered.append(product)

        # Step 2: Semantic fallback if filtering fails
        if not filtered:
            query_vec = MODEL.encode(user_message, convert_to_numpy=True)
            semantic_scores = []
            for idx, product in enumerate(ALL_PRODUCTS):
                if product.get("stock", 0) <= 0:
                    continue
                sim = 1 - cosine(query_vec, PRODUCT_EMBEDDINGS[idx])
                semantic_scores.append((sim, product))
            semantic_scores.sort(key=lambda x: x[0], reverse=True)
            filtered = [p for _, p in semantic_scores[:5]]

        if not filtered:
            dispatcher.utter_message("Sorry, I couldn't find any matching products.")
            return []

        # Step 3: Tailored output message
        top_products = filtered[:5]
        intro = "Here are some handpicked recommendations"
        if "category" in preferences:
            intro += f" for {preferences['category']}"
        if max_price:
            intro += f" under ₹{max_price}"
        intro += ":\n\n"

        response = intro
        for prod in top_products:
            specs = prod.get("specs", {})
            response += (
                f"🛒 *{prod['name']}* (₹{prod['price']})\n"
                f"👉 Brand: {prod['brand']} | Rating: ⭐ {prod.get('rating', 'N/A')}/5\n"
                f"💡 Display: {specs.get('display', 'N/A')} | Camera: {specs.get('camera', 'N/A')}\n"
                f"🔋 Battery: {specs.get('battery', 'N/A')} | Performance: {specs.get('performance', 'N/A')}\n"
                f"💾 Storage: {specs.get('storage', 'N/A')} | Color: {prod.get('color', 'N/A')}\n"
                f"🏷️ {prod.get('offers', 'No current offers')}\n"
                f"📌 {prod.get('description')}\n\n"
            )

        dispatcher.utter_message(text=response.strip())
        return []

