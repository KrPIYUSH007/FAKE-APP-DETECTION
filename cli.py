#!/usr/bin/env python3
"""
Interactive CLI for Fake App Detection
Place this file in the project root.
Run: python cli.py
"""

from src.colors import GREEN, RED, YELLOW, CYAN, BLUE, MAGENTA, RESET


import os
import sys
import textwrap
import pandas as pd

# Ensure `src` is importable
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# Import project modules
try:
    from scoring import calculate_risk
    from evidence import generate_evidence
    from takedown import generate_takedown_email
except Exception as e:
    print(RED + "ERROR importing src modules!" + RESET)
    print("Import error:", e)
    sys.exit(1)

# Paths
DATA_PATH = os.path.join(ROOT, "data", "apps.csv")
OUTPUT_DIR = os.path.join(ROOT, "output")
RESULTS_PATH = os.path.join(OUTPUT_DIR, "results.csv")
EVIDENCE_PATH = os.path.join(OUTPUT_DIR, "evidence.txt")
TAKEDOWN_PATH = os.path.join(OUTPUT_DIR, "takedown_email.txt")

# Default threshold (changed to 50)
THRESHOLD = 50


# -------------------------
# Utility Functions
# -------------------------

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    if not os.path.exists(DATA_PATH):
        print(RED + f"Data file not found: {DATA_PATH}" + RESET)
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)


# -------------------------
# 1. Run Detection
# -------------------------

def run_detection():
    df = load_data()
    if df.empty:
        print(RED + "No data loaded." + RESET)
        return df

    df["risk_score"] = df.apply(
        lambda row: calculate_risk(row["app_name"], row["publisher"]),
        axis=1
    )

    df_sorted = df.sort_values(by="risk_score", ascending=False).reset_index(drop=True)
    ensure_output_dir()
    df_sorted.to_csv(RESULTS_PATH, index=False)

    print(GREEN + f"[+] Detection complete — results saved to: {RESULTS_PATH}" + RESET)
    return df_sorted


# -------------------------
# 2. Show Results
# -------------------------

def show_results(df=None, top_n=20):
    if df is None:
        if os.path.exists(RESULTS_PATH):
            df = pd.read_csv(RESULTS_PATH)
        else:
            print(RED + "No results found. Run detection first." + RESET)
            return

    if df.empty:
        print(RED + "No results to show." + RESET)
        return

    pd.set_option("display.max_rows", None)
    print(CYAN + f"\n=== Detection Results (Top {top_n}) ===\n" + RESET)
    print(df.head(top_n)[["app_name", "package_name", "publisher", "risk_score"]].to_string(index=False))
    print()


# -------------------------
# 3. Generate Evidence
# -------------------------

def generate_evidence_files(df=None):
    if df is None:
        if os.path.exists(RESULTS_PATH):
            df = pd.read_csv(RESULTS_PATH)
        else:
            print(RED + "No results found. Run detection first." + RESET)
            return

    suspicious = df[df["risk_score"] >= THRESHOLD]
    ensure_output_dir()

    if suspicious.empty:
        print(YELLOW + f"No apps with risk_score >= {THRESHOLD}." + RESET)
        open(EVIDENCE_PATH, "w").close()
        return

    with open(EVIDENCE_PATH, "w", encoding="utf-8") as f:
        for _, row in suspicious.iterrows():
            ev = generate_evidence(row)
            f.write(ev + "\n")

    print(GREEN + f"[+] Evidence written to: {EVIDENCE_PATH}" + RESET)


# -------------------------
# 4. Show Evidence
# -------------------------

def show_evidence_file():
    if not os.path.exists(EVIDENCE_PATH):
        print(RED + "No evidence found. Run 'Generate Evidence' first." + RESET)
        return
    print(MAGENTA + "\n---- Evidence file preview ----\n" + RESET)
    print(open(EVIDENCE_PATH, "r", encoding="utf-8").read())
    print(MAGENTA + "\n---- end preview ----\n" + RESET)


# -------------------------
# 5. Generate Takedown Email
# -------------------------

def generate_takedown_for_top(df=None):
    if df is None:
        if os.path.exists(RESULTS_PATH):
            df = pd.read_csv(RESULTS_PATH)
        else:
            print(RED + "No results found. Run detection first." + RESET)
            return

    suspicious = df[df["risk_score"] >= THRESHOLD]

    if suspicious.empty:
        print(RED + f"No suspicious apps with risk_score >= {THRESHOLD}." + RESET)
        return

    top = suspicious.iloc[0]
    email_text = generate_takedown_email(
        top["app_name"],
        top["package_name"],
        top["publisher"],
        int(top["risk_score"])
    )

    ensure_output_dir()
    with open(TAKEDOWN_PATH, "w", encoding="utf-8") as f:
        f.write(email_text)

    print(GREEN + f"[+] Takedown email saved to: {TAKEDOWN_PATH}" + RESET)
    print("\n---- Email Preview ----\n")
    print(email_text)
    print("\n---- End ----\n")


# -------------------------
# 6. Check a single app manually (NEW FEATURE!)
# -------------------------

def check_single_app():
    print(CYAN + "\nEnter details of the app you want to evaluate:\n" + RESET)

    app_name = input("App name: ").strip()
    package = input("Package name: ").strip()
    publisher = input("Publisher: ").strip()

    if not app_name:
        print(RED + "App name is required." + RESET)
        return

    # 1) Calculate risk score
    score = calculate_risk(app_name, publisher)

    print(YELLOW + "\n--- App Evaluation ---" + RESET)
    print(f"App Name   : {app_name}")
    print(f"Package    : {package or '(not provided)'}")
    print(f"Publisher  : {publisher or '(not provided)'}")
    print(GREEN + f"Risk Score : {score}/100" + RESET)

    # 2) Generate evidence using a pseudo-row dict
    row = {
        "app_name": app_name,
        "package_name": package or "(not provided)",
        "publisher": publisher or "(not provided)",
        "risk_score": score
    }

    print(MAGENTA + "\n--- Evidence ---\n" + RESET)
    print(generate_evidence(row))

    # Optional: Save to CSV
    choice = input("Save this app into apps.csv for future detection? (y/n): ").strip().lower()
    if choice == "y":
        df = load_data()
        new_row = {
            "app_name": app_name,
            "package_name": package,
            "publisher": publisher,
            "is_official": "NO"
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_PATH, index=False)
        print(GREEN + "✔ App saved to dataset!" + RESET)


# -------------------------
# Main Menu
# -------------------------

def interactive_menu():
    global THRESHOLD
    df = None

    while True:
        print(CYAN + textwrap.dedent(f"""
        ================ Fake App Detection CLI ================
        Current threshold: {THRESHOLD}
        Choose an option:

        1) Run detection
        2) Show results
        3) Generate evidence file
        4) Show evidence file
        5) Generate takedown email
        6) Change threshold
        7) Reload data file
        8) Check a single app manually
        0) Exit
        """) + RESET)

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
                    print(GREEN + f"Threshold updated to {THRESHOLD}" + RESET)
                else:
                    print(RED + "Value out of range." + RESET)
            except:
                print(RED + "Invalid number." + RESET)
        elif choice == "7":
            df = load_data()
            print(GREEN + f"Loaded {len(df)} rows from apps.csv" + RESET)
        elif choice == "8":
            check_single_app()
        elif choice == "0":
            print(YELLOW + "Exiting... Goodbye!" + RESET)
            break
        else:
            print(RED + "Invalid choice. Try again." + RESET)


if __name__ == "__main__":
    interactive_menu()

