from scoring import OFFICIAL_APP_NAME, OFFICIAL_PUBLISHER

def generate_evidence(row):
    app = row["app_name"]
    package = row["package_name"]
    pub = row["publisher"]
    score = row["risk_score"]

    reasons = []

    if app.lower() != OFFICIAL_APP_NAME.lower():
        reasons.append(f"• Name mimics official app '{OFFICIAL_APP_NAME}'")

    if pub != OFFICIAL_PUBLISHER:
        reasons.append(f"• Publisher mismatch: '{pub}' (expected '{OFFICIAL_PUBLISHER}')")

    for keyword in ["update", "pro", "secure", "latest", "cashback"]:
        if keyword in app.lower():
            reasons.append(f"• Suspicious keyword found: '{keyword}'")
            break

    reason_text = "\n".join(reasons)

    return f"""
=============================
FAKE APP EVIDENCE REPORT
=============================

App Name       : {app}
Package        : {package}
Publisher      : {pub}
Risk Score     : {score}/100

Reasons for Suspicion:
{reason_text}

-------------------------------------------

"""
