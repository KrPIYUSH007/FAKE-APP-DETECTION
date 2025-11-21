from scoring import OFFICIAL_APP_NAME, OFFICIAL_PUBLISHER

def generate_takedown_email(app_name: str, package_name: str, publisher: str, risk_score: int) -> str:
    """
    Returns a formatted takedown email text.
    """
    email = f"""
Subject: Takedown Request – Fake App Impersonating {OFFICIAL_APP_NAME}

Dear Google Play Support,

We have detected a suspicious application that appears to impersonate the official {OFFICIAL_APP_NAME} app.

Official App:
- Name     : {OFFICIAL_APP_NAME}
- Publisher: {OFFICIAL_PUBLISHER}

Suspicious App:
- Name     : {app_name}
- Package  : {package_name}
- Publisher: {publisher}
- Risk Score: {risk_score}/100

Evidence:
- Name highly similar to the official app
- Publisher does not match the official publisher
- App name may mislead users into thinking this is an official update or premium version

We request you to review and take appropriate action to protect users from possible fraud.

Regards,
Hackathon Team
"""
    return email.strip("\n")
