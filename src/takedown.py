from brand_config import BRANDS

def generate_takedown_email(app_name, package_name, publisher, risk_score, brand):
    brand = brand.lower()
    cfg = BRANDS[brand]

    return f"""
To: App Store Compliance Team
Subject: URGENT — Fake {cfg['official_name']} Impersonator Detected

Dear team,

We have detected a malicious / impersonator app targeting the brand **{cfg['official_name']}**.

App details:
- App Name: {app_name}
- Package Name: {package_name}
- Publisher: {publisher}
- Risk Score: {risk_score}/100
- Official Publisher Should Be: {cfg['official_publisher']}

This app appears to mimic the official {cfg['official_name']} application and may mislead users.

We request immediate review and removal of this harmful app to prevent fraud or misuse.

Thank you,
Fake App Detection Team
"""
