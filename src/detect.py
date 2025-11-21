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
    print(f"{CYAN}\n🚀 Running Fake App Detection...\n{RESET}")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    df = pd.read_csv(DATA_PATH)

    df["risk_score"] = df.apply(
        lambda row: calculate_risk(row["app_name"], row["publisher"]),
        axis=1
    )

    df_sorted = df.sort_values(by="risk_score", ascending=False)
    results_path = os.path.join(OUTPUT_DIR, "results.csv")
    df_sorted.to_csv(results_path, index=False)

    print(f"{GREEN}✔ Detection complete!{RESET}")
    print(f"{YELLOW}Results saved to:{RESET} {results_path}\n")

    # Identify suspicious apps
    suspicious = df_sorted[df_sorted["risk_score"] >= 50]

    if suspicious.empty:
        print(f"{RED}No suspicious apps found with score ≥ 50{RESET}")
        return

    # Evidence
    evidence_path = os.path.join(OUTPUT_DIR, "evidence.txt")
    with open(evidence_path, "w") as f:
        for _, row in suspicious.iterrows():
            f.write(generate_evidence(row))
            f.write("\n")

    print(f"{GREEN}✔ Evidence file generated:{RESET} {evidence_path}")

    # Takedown email
    top = suspicious.iloc[0]
    email_text = generate_takedown_email(
        top["app_name"],
        top["package_name"],
        top["publisher"],
        int(top["risk_score"])
    )
    email_path = os.path.join(OUTPUT_DIR, "takedown_email.txt")
    with open(email_path, "w") as f:
        f.write(email_text)

    print(f"{GREEN}✔ Takedown email generated:{RESET} {email_path}\n")
    print(f"{CYAN}🎉 Fake App Detection Completed Successfully!{RESET}\n")

if __name__ == "__main__":
    main()

