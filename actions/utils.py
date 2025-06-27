# actions/utils.py
from sentence_transformers import SentenceTransformer

# Load efficient transformer model (free and fast)
MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# Mock database of products in realistic format
ALL_PRODUCTS = [
    {
        "id": 101,
        "name": "Samsung Galaxy S23",
        "brand": "Samsung",
        "category": "phone",
        "price": 699,
        "stock": 15,
        "color": "black",
        "offers": "15% off",
        "rating": 4.5,
        "image_url": "https://example.com/s23.jpg",
        "specs": {
            "battery": "4500mAh",
            "camera": "50MP Triple",
            "display": "6.1 inch AMOLED",
            "performance": "Snapdragon 8 Gen 2",
            "storage": "128GB",
            "ram": "8GB",
            "charging": "25W fast charging"
        },
        "description": "Premium flagship phone with vibrant AMOLED screen and excellent camera."
    },
    {
        "id": 102,
        "name": "Apple iPhone 14",
        "brand": "Apple",
        "category": "phone",
        "price": 799,
        "stock": 10,
        "color": "blue",
        "offers": "10% off",
        "rating": 4.7,
        "image_url": "https://example.com/iphone14.jpg",
        "specs": {
            "battery": "3279mAh",
            "camera": "12MP Dual",
            "display": "6.1 inch OLED",
            "performance": "A15 Bionic",
            "storage": "128GB",
            "ram": "6GB",
            "charging": "20W fast charging"
        },
        "description": "The latest iPhone with top-notch performance and camera."
    },
    {
        "id": 201,
        "name": "Dell XPS 13",
        "brand": "Dell",
        "category": "laptop",
        "price": 999,
        "stock": 5,
        "color": "silver",
        "offers": "10% off",
        "rating": 4.6,
        "image_url": "https://example.com/xps13.jpg",
        "specs": {
            "battery": "52Wh",
            "camera": "720p HD",
            "display": "13.4 inch FHD+",
            "performance": "Intel i7 11th Gen",
            "storage": "512GB SSD",
            "ram": "16GB",
            "charging": "65W USB-C"
        },
        "description": "Compact, portable laptop with excellent battery life and sleek design."
    },
    # Add more devices across categories: smartwatch, tablet, headphones, etc.
]

# Sentence embeddings for semantic fallback
PRODUCT_EMBEDDINGS = MODEL.encode(
    [p["description"] for p in ALL_PRODUCTS],
    convert_to_numpy=True
)

# Policies for returns, shipping, and warranty
POLICIES = {
    "return": (
        "You may return most new, unopened items within 30 days of delivery for a full refund. "
        "We cover return shipping for incorrect or defective items. Refunds are processed in 5–7 days."
    ),
    "shipping": (
        "We offer standard (3–5 days), expedited (1–2 days), and next-day delivery. Shipping is calculated at checkout."
    ),
    "warranty": (
        "All electronic items come with a 1-year manufacturer warranty. Extended warranties available at checkout."
    )
}

