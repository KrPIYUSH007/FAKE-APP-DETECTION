#!/usr/bin/env python3
"""
Multi‑Brand Fake App Detection
(PhonePe / Paytm / GPay)
Batch detection script — NOT the CLI.
"""

import os
import pandas as pd

# Correct imports for running from project root
from src.colors import GREEN, RED, YELLOW, CYAN, RESET
from src.scoring import calculate_risk
from src.evidence import generate_evidence
from src.takedown import generate_takedown_email

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))        # detects/scripts folder
ROOT_DIR = os.path.dirname(BASE_DIR)                         # project root
DATA_PATH = os.path.join(ROOT_DIR, "data", "apps.csv")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")


def main():
    print(f"{CYAN}\n🚀 Running Multi‑Brand Fake App Detection...\n{RESET}")

    # Ensure output folder exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Load CSV
    if not os.path.exists(DATA_PATH):
        print(f"{RED}❌ ERROR: apps.csv not found at {DATA_PATH}{RESET}")
        return

    df = pd.read_csv(DATA_PATH)

    # Required columns
    required_cols = {"app_name", "package_name", "publisher", "brand"}
    if not required_cols.issubset(df.columns):
        print(f"{RED}❌ ERROR: CSV missing required columns: {required_cols}{RESET}")
        return

    # ---- Compute multi‑brand risk score ----
    df["risk_score"] = df.apply(
        lambda row: calculate_risk(
            row["app_name"],
            row["publisher"],
            row["brand"].lower().strip()
        ),
        axis=1
    )

    # ---- Sort by risk ----
    df_sorted = df.sort_values(by="risk_score", ascending=False)
    results_path = os.path.join(OUTPUT_DIR, "results.csv")
    df_sorted.to_csv(results_path, index=False)

    print(f"{GREEN}✔ Detection complete!{RESET}")
    print(f"{YELLOW}📄 Results saved to:{RESET} {results_path}\n")

    # ---- Filter suspicious apps ----
    SUSPICIOUS_THRESHOLD = 50
    suspicious = df_sorted[df_sorted["risk_score"] >= SUSPICIOUS_THRESHOLD]

    if suspicious.empty:
        print(f"{RED}❗ No suspicious apps found with score ≥ {SUSPICIOUS_THRESHOLD}{RESET}")
        return

    # ---- Generate Evidence File ----
    evidence_path = os.path.join(OUTPUT_DIR, "evidence.txt")
    with open(evidence_path, "w", encoding="utf-8") as f:
        for _, row in suspicious.iterrows():
            f.write(generate_evidence(row) + "\n\n")

    print(f"{GREEN}✔ Evidence file generated:{RESET} {evidence_path}")

    # ---- Generate Takedown Email for Top App ----
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
