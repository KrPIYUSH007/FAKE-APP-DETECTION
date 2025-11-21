import json
import os
from similarity import name_similarity

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BRANDS_FILE = os.path.join(BASE_DIR, "data", "brands.json")

# Load brand configuration
with open(BRANDS_FILE, "r") as f:
    BRANDS = json.load(f)

def calculate_risk(app_name: str, publisher: str, brand: str) -> int:
    """
    Multi-brand scoring for PhonePe / Paytm / GPay.
    """
    brand = brand.lower().strip()
    if brand not in BRANDS:
        return 0

    cfg = BRANDS[brand]

    official_name = cfg["official_name"]
    official_pub = cfg["official_publisher"]
    keywords = cfg["keywords"]
    threshold = cfg["similarity_threshold"]
    aliases = cfg.get("aliases", [])

    score = 0
    name_low = app_name.lower()

    # 1. Name similarity to official name
    sim = name_similarity(app_name, official_name)
    if sim >= threshold:
        score += 50

    # 2. Check aliases (PhonePay, Pay tm, Gpay etc)
    for a in aliases:
        if a in name_low:
            score += 30
            break

    # 3. Publisher mismatch
    if publisher != official_pub:
        score += 30

    # 4. Suspicious keywords
    if any(k in name_low for k in keywords):
        score += 20

    return min(score, 100)
