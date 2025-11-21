 Fake App Detection System
Identify Fake / Impersonator Apps Targeting PhonePe

A rule‑based PhonePe app fraud detection engine powered by Python.

 Overview
The PhonePe Fake App Detection System analyzes app metadata to find fake or impersonator apps pretending to be PhonePe on app stores.

It assigns a risk score (0–100) based on:

Name similarity

Fake/unknown publisher

Suspicious keywords

Alias usage

Brand mismatch

The tool also generates:

✔ Evidence report
✔ Takedown email
✔ Ranked results table
✔ Manual app analysis

This project includes a clean CLI interface.

 Project Structure
FAKE-APP-DETECTION/
│
├── data/
│   └── apps.csv                # Input dataset (PhonePe apps only)
│
├── output/
│   ├── results.csv             # Detection results
│   ├── evidence.txt            # Evidence report
│   └── takedown_email.txt      # Auto-generated email
│
├── src/
│   ├── scoring.py
│   ├── evidence.py
│   ├── takedown.py
│   ├── similarity.py
│   ├── brand_config.py         # Only PhonePe configuration now
│   └── colors.py
│
├── cli.py                      # Interactive CLI application
└── README.md                   # Documentation


        ---Features---
Single-Brand Detection (PhonePe)
Detects impersonators for:
Smart Risk Scoring
Risk score uses:

Name similarity (SequenceMatcher)

Publisher mismatch

Suspicious keywords (reward, cashback, update, secure)

Official PhonePe configuration rules

Alias detection (“phonepay”, “phone pe”, “fonepe”)

Automatic Evidence Generation
Produces a detailed evidence summary per suspicious app.

Automatic Takedown Email
Creates a ready‑to‑send email for PhonePe / Play Store compliance.

Interactive CLI Menu
Includes options like:

Run full detection

Display results

Generate evidence

Manual app analysis

Change detection threshold

Reload dataset

Screenshots
CLI Menu

 Sample Results

 Evidence Report

Add actual screenshots in assets/ and update paths if needed.

-----Installation------
1️⃣ Clone Repository
git clone https://github.com/<your-username>/fake-app-detection.git
cd fake-app-detection
2️⃣ Install Dependencies
pip install pandas
▶️ Usage
Run the tool:

python cli.py
You will see:

============ PhonePe Fake App Detection CLI ============
1) Run detection
2) Show results
3) Generate evidence file
4) Show evidence
5) Generate takedown email
6) Change threshold
7) Reload CSV
8) Manual app check
0) Exit
🗂 Data Format (apps.csv)
Your dataset must follow:

app_name,package_name,publisher,brand
PhonePe Cashback,com.fake.reward,Reward Lab,phonepe
Phone Pe UPI Guide,com.phonepe.upi.guide,Guide Studio,phonepe
✔ brand must always be: phonepe

 Customization
PhonePe rules live in:

src/brand_config.py
Example:

"phonepe": {
    "official_name": "PhonePe",
    "official_publisher": "PhonePe Pvt Ltd",
    "aliases": ["phonepay", "phone pe", "fonepe"],
    "keywords": ["reward", "cashback", "secure", "update"]
}
 Future Enhancements
GUI (Tkinter / PyQt / CustomTkinter)

Real-time Play Store scraper

Image/icon similarity detection

Machine learning fraud detection

Contributors
Name	                                    Role	                              GitHub
Omkar Kumar	                          Developer Head	                      https://github.com/omkarrkr
Niketh P	                          Developer & Testing	                  https://github.com/nikethp33 
Paleti Hithaishi Hrushikesh	          Dataset Handling & Documentation	      https://github.com/hitz-codes
Piyush Kumar	                      Project Lead & Developer	              https://github.com/KrPIYUSH007



