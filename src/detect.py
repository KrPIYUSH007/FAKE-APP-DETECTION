import os
import pandas as pd

from scoring import calculate_risk
from evidence import generate_evidence
from takedown import generate_takedown_email

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, "data", "apps.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

def main():
    # Ensure output folder exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Load dataset
    df = pd.read_csv(DATA_PATH)

    # 2. Calculate risk score for each app
    df["risk_score"] = df.apply(
        lambda row: calculate_risk(row["app_name"], row["publisher"]),
        axis=1
    )

    # 3. Sort by risk score (highest first)
    df_sorted = df.sort_values(by="risk_score", ascending=False)

    print("=== Fake App Detection Results ===\n")
    print(df_sorted[["app_name", "package_name", "publisher", "risk_score"]])

    # 4. Save full results to CSV
    results_path = os.path.join(OUTPUT_DIR, "results.csv")
    df_sorted.to_csv(results_path, index=False)
    print(f"\n[+] Saved full results to: {results_path}")

    # 5. Filter suspicious apps (risk >= 60)
    suspicious = df_sorted[df_sorted["risk_score"] >= 60]

    if suspicious.empty:
        print("\nNo suspicious apps found with risk_score >= 60.")
        return

    # 6. Generate evidence for each suspicious app
    evidence_path = os.path.join(OUTPUT_DIR, "evidence.txt")
    with open(evidence_path, "w", encoding="utf-8") as f:
        for _, row in suspicious.iterrows():
            ev = generate_evidence(row)
            f.write(ev + "\n")

    print(f"[+] Evidence generated for suspicious apps in: {evidence_path}")

    # 7. Generate takedown email for the top suspicious app
    top = suspicious.iloc[0]
    email_text = generate_takedown_email(
        app_name=top["app_name"],
        package_name=top["package_name"],
        publisher=top["publisher"],
        risk_score=int(top["risk_score"])
    )

    email_path = os.path.join(OUTPUT_DIR, "takedown_email.txt")
    with open(email_path, "w", encoding="utf-8") as f:
        f.write(email_text)

    print(f"[+] Takedown email for top suspicious app saved to: {email_path}")

if __name__ == "__main__":
    main()
