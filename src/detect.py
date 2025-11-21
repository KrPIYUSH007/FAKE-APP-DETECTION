#!/usr/bin/env python3
"""
Multi‑Brand Fake App Detection (PhonePe / Paytm / GPay)
Batch detection script — NOT the CLI.
"""

import os
import pandas as pd

from colors import GREEN, RED, YELLOW, CYAN, RESET
from scoring import calculate_risk
from evidence import generate_evidence
from takedown import generate_takedown_email

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "apps.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def main():
    print(f"{CYAN}\n🚀 Running Multi‑Brand Fake App Detection...\n{RESET}")

    # ensure output folder exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # load CSV (MUST include: app_name, package_name, publisher, brand)
    df = pd.read_csv(DATA_PATH)

    required_cols = {"app_name", "package_name", "publisher", "brand"}
    if not required_cols.issubset(set(df.columns)):
        print(f"{RED}❌ ERROR: CSV missing required columns: {required_cols}{RESET}")
        return

    # compute risk using the NEW multi‑brand scoring
    df["risk_score"] = df.apply(
        lambda row: calculate_risk(
            row["app_name"],
            row["publisher"],
            row["brand"].lower().strip(),
        ),
        axis=1
    )

    # sort results
    df_sorted = df.sort_values(by="risk_score", ascending=False)
    results_path = os.path.join(OUTPUT_DIR, "results.csv")
    df_sorted.to_csv(results_path, index=False)

    print(f"{GREEN}✔ Detection complete!{RESET}")
    print(f"{YELLOW}Results saved to:{RESET} {results_path}\n")

    # suspicious threshold
    SUSPICIOUS_THRESHOLD = 50
    suspicious = df_sorted[df_sorted["risk_score"] >= SUSPICIOUS_THRESHOLD]

    if suspicious.empty:
        print(f"{RED}❗ No suspicious apps found with score ≥ {SUSPICIOUS_THRESHOLD}{RESET}")
        return

    # generate evidence file
    evidence_path = os.path.join(OUTPUT_DIR, "evidence.txt")
    with open(evidence_path, "w", encoding="utf-8") as f:
        for _, row in suspicious.iterrows():
            ev = generate_evidence(row)
            f.write(ev + "\n")

    print(f"{GREEN}✔ Evidence file generated:{RESET} {evidence_path}")

    # generate takedown email for TOP suspicious app
    top = suspicious.iloc[0]
    email_text = generate_takedown_email(
        app_name=top["app_name"],
        package_name=top["package_name"],
        publisher=top["publisher"],
        risk_score=int(top["risk_score"]),
        brand=top["brand"]
    )

    email_path = os.path.join(OUTPUT_DIR, "takedown_email.txt")
    with open(email_path, "w", encoding="utf-8") as f:
        f.write(email_text)

    print(f"{GREEN}✔ Takedown email generated:{RESET} {email_path}")
    print(f"{CYAN}🎉 Multi‑Brand Fake App Detection Completed Successfully!{RESET}\n")


if __name__ == "__main__":
    main()
