from brand_config import BRANDS

def generate_evidence(row):
    brand = row["brand"].lower()
    cfg = BRANDS[brand]

    reasons = []

    # Reason list
    if row["publisher"] != cfg["official_publisher"]:
        reasons.append(f"- Publisher mismatch (found: {row['publisher']}, expected: {cfg['official_publisher']})")

    lower_name = row["app_name"].lower()
    for k in cfg["keywords"]:
        if k in lower_name:
            reasons.append(f"- Contains suspicious keyword: '{k}'")
            break

    for alias in cfg.get("aliases", []):
        if alias in lower_name:
            reasons.append(f"- Matches known typosquat pattern: '{alias}'")
            break

    text = f"""
==============================
EVIDENCE REPORT — {row['app_name']}
Brand: {brand.upper()}
Risk Score: {row['risk_score']}
Package: {row['package_name']}
Publisher: {row['publisher']}
==============================

Reasons:
{chr(10).join(reasons) if reasons else "No suspicious indicators found"}

"""
    return text
