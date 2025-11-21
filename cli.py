#!/usr/bin/env python3
"""
Interactive CLI for Multi‑Brand Fake App Detection
Supports PhonePe / Paytm / GPay
"""

import os
import sys
import textwrap
import pandas as pd

# ---------- Import color theme ----------
from src.colors import GREEN, RED, YELLOW, CYAN, BLUE, MAGENTA, RESET

# ---------- Ensure src/ is in path ----------
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(ROOT, "src")
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

# ---------- Import project modules ----------
from src.scoring import calculate_risk
from src.evidence import generate_evidence
from src.takedown import generate_takedown_email

# ---------- File paths ----------
DATA_PATH = os.path.join(ROOT, "data", "apps.csv")
OUTPUT_DIR = os.path.join(ROOT, "output")
RESULTS_PATH = os.path.join(OUTPUT_DIR, "results.csv")
EVIDENCE_PATH = os.path.join(OUTPUT_DIR, "evidence.txt")
TAKEDOWN_PATH = os.path.join(OUTPUT_DIR, "takedown_email.txt")

# Default threshold
THRESHOLD = 50

# Current brand (used only for manual app check)
CURRENT_BRAND = "phonepe"

# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def load_data():
    if not os.path.exists(DATA_PATH):
        print(RED + f"Data file not found: {DATA_PATH}" + RESET)
        return pd.DataFrame()
    return pd.read_csv(DATA_PATH)

# ============================================================
# BRAND SWITCHER
# ============================================================

def choose_brand():
    global CURRENT_BRAND
    print(CYAN + "\nChoose Brand:\n" + RESET)
    print("1) PhonePe")
    print("2) Paytm")
    print("3) GPay")

    choice = input("Enter choice: ").strip()
    if choice == "1":
        CURRENT_BRAND = "phonepe"
    elif choice == "2":
        CURRENT_BRAND = "paytm"
    elif choice == "3":
        CURRENT_BRAND = "gpay"
    else:
        print(RED + "Invalid choice. Keeping previous brand." + RESET)

    print(GREEN + f"\nCurrent brand for manual checks: {CURRENT_BRAND.upper()}\n" + RESET)

# ============================================================
# 1. RUN DETECTION
# ============================================================

def run_detection():
    df = load_data()
    if df.empty:
        print(RED + "No data loaded." + RESET)
        return df

    required = {"app_name", "package_name", "publisher", "brand"}
    if not required.issubset(df.columns):
        print(RED + f"CSV ERROR: Missing required columns: {required}" + RESET)
        return df

    df["risk_score"] = df.apply(
        lambda row: calculate_risk(
            row["app_name"], row["publisher"], row["brand"]
        ),
        axis=1
    )

    df_sorted = df.sort_values(by="risk_score", ascending=False).reset_index(drop=True)

    ensure_output_dir()
    df_sorted.to_csv(RESULTS_PATH, index=False)

    print(GREEN + f"\n[+] Detection complete — saved to {RESULTS_PATH}\n" + RESET)
    return df_sorted

# ============================================================
# 2. SHOW RESULTS
# ============================================================

def show_results(df=None, top_n=20):
    if df is None:
        if os.path.exists(RESULTS_PATH):
            df = pd.read_csv(RESULTS_PATH)
        else:
            print(RED + "Run detection first." + RESET)
            return

    print(CYAN + f"\n=== Detection Results (Top {top_n}) ===\n" + RESET)
    print(df.head(top_n)[["app_name", "package_name", "brand", "publisher", "risk_score"]]
          .to_string(index=False))
    print()

# ============================================================
# 3. GENERATE EVIDENCE
# ============================================================

def generate_evidence_files(df=None):
    if df is None:
        if os.path.exists(RESULTS_PATH):
            df = pd.read_csv(RESULTS_PATH)
        else:
            print(RED + "Run detection first." + RESET)
            return

    suspicious = df[df["risk_score"] >= THRESHOLD]
    ensure_output_dir()

    if suspicious.empty:
        print(YELLOW + f"No suspicious apps (>= {THRESHOLD}) found." + RESET)
        open(EVIDENCE_PATH, "w").close()
        return

    with open(EVIDENCE_PATH, "w", encoding="utf-8") as f:
        for _, row in suspicious.iterrows():
            f.write(generate_evidence(row) + "\n")

    print(GREEN + f"[+] Evidence saved to: {EVIDENCE_PATH}\n" + RESET)

# ============================================================
# 4. SHOW EVIDENCE
# ============================================================

def show_evidence_file():
    if not os.path.exists(EVIDENCE_PATH):
        print(RED + "No evidence file. Generate first." + RESET)
        return

    print(MAGENTA + "\n---- EVIDENCE PREVIEW ----\n" + RESET)
    print(open(EVIDENCE_PATH, "r", encoding="utf-8").read())
    print(MAGENTA + "\n---- END ----\n" + RESET)

# ============================================================
# 5. GENERATE TAKEDOWN EMAIL
# ============================================================

def generate_takedown_for_top(df=None):
    if df is None:
        if os.path.exists(RESULTS_PATH):
            df = pd.read_csv(RESULTS_PATH)
        else:
            print(RED + "Run detection first." + RESET)
            return

    suspicious = df[df["risk_score"] >= THRESHOLD]

    if suspicious.empty:
        print(RED + "No suspicious apps found." + RESET)
        return

    top = suspicious.iloc[0]

    email = generate_takedown_email(
        top["app_name"],
        top["package_name"],
        top["publisher"],
        int(top["risk_score"]),
        top["brand"]
    )

    ensure_output_dir()
    with open(TAKEDOWN_PATH, "w", encoding="utf-8") as f:
        f.write(email)

    print(GREEN + f"[+] Takedown email saved: {TAKEDOWN_PATH}\n" + RESET)
    print(email)

# ============================================================
# 6. MANUAL SINGLE APP CHECK
# ============================================================

def check_single_app():
    print(CYAN + f"\nManual Check (Brand = {CURRENT_BRAND.upper()})\n" + RESET)

    app_name = input("App Name: ").strip()
    package = input("Package Name: ").strip()
    publisher = input("Publisher: ").strip()

    score = calculate_risk(app_name, publisher, CURRENT_BRAND)

    print(YELLOW + "\n--- ANALYSIS ---" + RESET)
    print(f"App Name    : {app_name}")
    print(f"Publisher   : {publisher}")
    print(f"Brand       : {CURRENT_BRAND.upper()}")
    print(GREEN + f"Risk Score  : {score}/100\n" + RESET)

    row = {
        "app_name": app_name,
        "package_name": package,
        "publisher": publisher,
        "brand": CURRENT_BRAND,
        "risk_score": score
    }

    print(MAGENTA + "\n--- Evidence ---\n" + RESET)
    print(generate_evidence(row))

# ============================================================
# MAIN MENU
# ============================================================

def interactive_menu():
    global THRESHOLD
    df = None

    while True:
        print(CYAN + textwrap.dedent(f"""
        ============ Fake App Detection CLI ============
        Brand (manual mode): {CURRENT_BRAND.upper()}
        Threshold: {THRESHOLD}

        1) Run detection
        2) Show results
        3) Generate evidence file
        4) Show evidence
        5) Generate takedown email
        6) Change threshold
        7) Reload CSV
        8) Manual check (single app)
        9) Change brand
        0) Exit
        """) + RESET)

        choice = input("Enter choice: ").strip()

        if choice == "1": df = run_detection()
        elif choice == "2": show_results(df)
        elif choice == "3": generate_evidence_files(df)
        elif choice == "4": show_evidence_file()
        elif choice == "5": generate_takedown_for_top(df)
        elif choice == "6":
            THRESHOLD = int(input("Enter new threshold (0–100): "))
        elif choice == "7":
            df = load_data()
            print(GREEN + f"Reloaded CSV: {len(df)} rows" + RESET)
        elif choice == "8":
            check_single_app()
        elif choice == "9":
            choose_brand()
        elif choice == "0":
            print(YELLOW + "Goodbye!" + RESET)
            break
        else:
            print(RED + "Invalid option." + RESET)

if __name__ == "__main__":
    interactive_menu()
