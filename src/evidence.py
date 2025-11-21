from scoring import OFFICIAL_APP_NAME, OFFICIAL_PUBLISHER

def generate_evidence(row) -> str:
    """
    Takes a pandas row and returns a formatted evidence string.
    """
    reasons = []

    app_name = row["app_name"]
    publisher = row["publisher"]
    risk_score = row["risk_score"]

    # Reason 1: similar name
    if app_name.lower().replace(" ", "") != OFFICIAL_APP_NAME.lower().replace(" ", ""):
        reasons.append(f'- Name is similar to official app "{OFFICIAL_APP_NAME}"')

    # Reason 2: publisher mismatch
    if publisher != OFFICIAL_PUBLISHER:
        reasons.append(f'- Publisher mismatch: "{publisher}" vs official "{OFFICIAL_PUBLISHER}"')

    # Reason 3: keywords
    suspicious_words = []
    for word in ["update", "pro", "secure", "latest", "cashback"]:
        if word in app_name.lower():
            suspicious_words.append(word)
    if suspicious_words:
        reasons.append(f'- Contains suspicious keywords in app name: {", ".join(suspicious_words)}')

    if not reasons:
        reasons.append("- Heuristic detection triggered, but no specific reason recorded.")

    reasons_text = "\n".join(reasons)

    evidence = f"""
=============================
EVIDENCE FOR SUSPECT APP
=============================

App Name   : {app_name}
Package    : {row["package_name"]}
Publisher  : {publisher}
Risk Score : {risk_score}

Reasons:
{reasons_text}

"""
    return evidence
