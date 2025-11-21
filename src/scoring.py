from similarity import name_similarity

OFFICIAL_APP_NAME = "PhonePe"
OFFICIAL_PUBLISHER = "PhonePe Pvt Ltd"
SUSPICIOUS_KEYWORDS = ["update", "pro", "secure", "latest", "cashback"]

def calculate_risk(app_name: str, publisher: str) -> int:
    """
    Returns a risk score from 0 to 100 using:
    - name similarity
    - publisher mismatch
    - suspicious keywords in app name
    """
    score = 0

    # 1. LOWERED THRESHOLD so fake apps get flagged
    sim = name_similarity(app_name, OFFICIAL_APP_NAME)
    if sim > 0.70:    
        score += 50   

    # 2. Publisher mismatch
    if publisher != OFFICIAL_PUBLISHER:
        score += 30

    # 3. Suspicious keywords (update, pro, secure…)
    lower_name = app_name.lower()
    if any(word in lower_name for word in SUSPICIOUS_KEYWORDS):
        score += 20

    return min(score, 100)
