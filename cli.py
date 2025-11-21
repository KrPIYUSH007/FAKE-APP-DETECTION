#!/usr/bin/env python3
"""
Simple interactive CLI for the fake-app-detection project.

Place this file in the project root (next to `data/`, `src/`, `output/`).
Run: python cli.py
"""

import os
import sys
import textwrap
import pandas as pd

# Ensure `src` is importable
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Import functions from your src files
try:
    from scoring import calculate_risk
    from evidence import generate_evidence
    from takedown import generate_takedown_email
except Exception as e:
    print("ERROR importing src modules. Make sure 'src' directory exists and files are present.")
    print("Import error:", e)
    sys.exit(1)

DATA_PATH = os.path.join(ROOT, "data", "apps.csv")
OUTPUT_DIR = os.path.join(ROOT, "output")
RESULTS_PATH = os.path.join(OUTPUT_DIR, "results.csv")
EVIDENCE_PATH = os.path.join(OUTPUT_DIR, "evidence.txt")
TAKEDOWN_PATH = os.path.join(OUTPUT_DIR, "takedown_email.txt")

# default threshold
THRESHOLD = 60

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    if not os.path.exists(DATA_PATH):
        print(f"Data file not found: {DATA_PATH}")
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)

def run_detection():
    df = load_data()
    if df.empty:
        print("No data loaded.")
        return df

    df["risk_score"] = df.apply(
        lambda row: calculate_risk(row["app_name"], row["publisher"]),
        axis=1
    )
    df_sorted = df.sort_values(by="risk_score", ascending=False).reset_index(drop=True)
    ensure_output_dir()
    df_sorted.to_csv(RESULTS_PATH, index=False)
    print(f"[+] Detection complete — results saved to: {RESULTS_PATH}")
    return df_sorted

def show_results(df=None, top_n=20):
    if df is None:
        if os.path.exists(RESULTS_PATH):
            df = pd.read_csv(RESULTS_PATH)
        else:
            print("No results found. Run detection first.")
            return
    if df.empty:
        print("No results to show.")
        return
    pd.set_option("display.max_rows", None)
    print("\n=== Detection Results (Top {}) ===".format(top_n))
    print(df.head(top_n)[["app_name", "package_name", "publisher", "risk_score"]].to_string(index=False))
    print()

def generate_evidence_files(df=None):
    if df is None:
        if os.path.exists(RESULTS_PATH):
            df = pd.read_csv(RESULTS_PATH)
        else:
            print("No results found. Run detection first.")
            return
    suspicious = df[df["risk_score"] >= THRESHOLD]
    ensure_output_dir()
    if suspicious.empty:
        print(f"No apps with risk_score >= {THRESHOLD}.")
        # clear evidence if exists
        open(EVIDENCE_PATH, "w").close()
        return
    with open(EVIDENCE_PATH, "w", encoding="utf-8") as f:
        for _, row in suspicious.iterrows():
            ev = generate_evidence(row)
            f.write(ev + "\n")
    print(f"[+] Evidence written to: {EVIDENCE_PATH}")

def generate_takedown_for_top(df=None):
    if df is None:
        if os.path.exists(RESULTS_PATH):
            df = pd.read_csv(RESULTS_PATH)
        else:
            print("No results found. Run detection first.")
            return
    suspicious = df[df["risk_score"] >= THRESHOLD]
    if suspicious.empty:
        print(f"No suspicious apps with risk_score >= {THRESHOLD}.")
        return
    top = suspicious.iloc[0]
    email_text = generate_takedown_email(
        app_name=top["app_name"],
        package_name=top["package_name"],
        publisher=top["publisher"],
        risk_score=int(top["risk_score"])
    )
    ensure_output_dir()
    with open(TAKEDOWN_PATH, "w", encoding="utf-8") as f:
        f.write(email_text)
    print(f"[+] Takedown email for top suspicious app saved to: {TAKEDOWN_PATH}")
    print("\n---- Takedown email preview ----")
    print(textwrap.dedent(email_text))
    print("---- end preview ----\n")

def show_evidence_file():
    if not os.path.exists(EVIDENCE_PATH):
        print("No evidence file found. Run 'Generate Evidence' first.")
        return
    print("\n---- Evidence file preview ----\n")
    print(open(EVIDENCE_PATH, "r", encoding="utf-8").read())
    print("\n---- end preview ----\n")

def interactive_menu():
    global THRESHOLD
    df = None
    while True:
        print(textwrap.dedent(f"""
        ================= Fake App Detection CLI =================
        Current threshold: {THRESHOLD} (apps with risk_score >= threshold are 'suspicious')
        Choose an option:
        1) Run detection (compute risk scores and save results)
        2) Show results (top 20)
        3) Generate evidence file for suspicious apps
        4) Show evidence file
        5) Generate takedown email for top suspicious app
        6) Change threshold
        7) Reload data file
        0) Exit
        """))
        choice = input("Enter choice: ").strip()
        if choice == "1":
            df = run_detection()
        elif choice == "2":
            show_results(df)
        elif choice == "3":
            if df is None and os.path.exists(RESULTS_PATH):
                df = pd.read_csv(RESULTS_PATH)
            generate_evidence_files(df)
        elif choice == "4":
            show_evidence_file()
        elif choice == "5":
            if df is None and os.path.exists(RESULTS_PATH):
                df = pd.read_csv(RESULTS_PATH)
            generate_takedown_for_top(df)
        elif choice == "6":
            val = input("Enter new threshold (0-100): ").strip()
            try:
                v = int(val)
                if 0 <= v <= 100:
                    THRESHOLD = v
                    print(f"Threshold updated to {THRESHOLD}")
                else:
                    print("Value out of range.")
            except:
                print("Invalid number.")
        elif choice == "7":
            df = load_data()
            if not df.empty:
                print(f"Loaded {len(df)} rows from data file.")
        elif choice == "0":
            print("Exiting. Bye!")
            break
        else:
            print("Unknown option. Try again.")

if __name__ == "__main__":
    interactive_menu()
