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

    # 1. Name similarity with official app
    sim = name_similarity(app_name, OFFICIAL_APP_NAME)
    if sim > 0.8:
        score += 50   # very similar name

    # 2. Publisher mismatch
    if publisher != OFFICIAL_PUBLISHER:
        score += 30   # not official publisher

    # 3. Suspicious keywords
    lower_name = app_name.lower()
    if any(word in lower_name for word in SUSPICIOUS_KEYWORDS):
        score += 20   # contains “update”, “pro”, etc.

    # Cap max at 100
    return min(score, 100)
